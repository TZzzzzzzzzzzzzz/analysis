#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@Author: TZ
@Date: 2024/09/06 11:50
@Desc: This module contains functions for creating new features, modifying existing features, 
       and selecting important features to improve model performance.
'''


from .config import VISUALIZATION_CONFIG
from .report_generation import PDF
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import math


def visualize_features(data, feature_list, pdf=None) -> None:
    '''Visualize selected features from the dataset.

    Args:
        data (pd.DataFrame): The input DataFrame containing the data.
        feature_list (list): A list of feature names to visualize.

    Returns:
        None: This function does not return any value but visualizes the features.

    Description:
        This function plots histograms for the selected features and scatter plots 
        between each feature and the target variable. It saves the figures to files.
    '''

    print('+------------------------------------------------------------------------------------------------------------+')
    print('                                         -Visualize Features-')


    # Plot histograms for selected features
    sub_data = data[feature_list]
    sub_data.hist(bins=VISUALIZATION_CONFIG['hist_bins'], 
                  figsize=(VISUALIZATION_CONFIG['plot_width_subplots'], VISUALIZATION_CONFIG['plot_height_subplots']),
                  color=VISUALIZATION_CONFIG['hist_color'], 
                  alpha=VISUALIZATION_CONFIG['hist_alpha'],
                  edgecolor=VISUALIZATION_CONFIG['hist_edgecolor'],
                  )
    plt.suptitle('Histograms for Selected Features', fontsize=VISUALIZATION_CONFIG['title_font_size'])
    plt.tight_layout()
    plt.savefig('reports/figures/feature_histograms.png', dpi=VISUALIZATION_CONFIG['resolution'])
    print('Histograms for selected features saved to reports/figures/feature_histograms.png')

    # Plot scatter plots for features vs. target variable
    target = data.columns[-1]
    features = data.columns[:-1]
    n_cols = math.ceil(math.sqrt(len(features))) 
    n_rows = math.ceil(len(features) / n_cols)
    plt.figure(figsize=(VISUALIZATION_CONFIG['plot_width_subplots'], VISUALIZATION_CONFIG['plot_height_subplots']))
    for i, feature in enumerate(features):
        plt.subplot(n_rows, n_cols, i + 1)
        plt.scatter(data[feature], data[target],                     
                    alpha=VISUALIZATION_CONFIG['scatter_alpha'],
                    color=VISUALIZATION_CONFIG['scatter_color'],
                    s=VISUALIZATION_CONFIG['scatter_size'],
                    marker=VISUALIZATION_CONFIG['scatter_marker'])
        plt.xlabel(feature)
        plt.ylabel(target)
    plt.suptitle('Scatter Plots for Features vs. Target Variable', fontsize=VISUALIZATION_CONFIG['title_font_size'])
    plt.tight_layout()
    plt.savefig('reports/figures/feature_scatter_plots.png', dpi=VISUALIZATION_CONFIG['resolution'])
    print('Scatter plots for features vs. target variable saved to reports/figures/feature_scatter_plots.png')

    if pdf != None:
        pdf.chapter_body('Visualize selected features.')
        pdf.chapter_body('Feature Histograms')
        pdf.add_image('reports/figures/feature_histograms.png')
        pdf.add_page()
        pdf.chapter_body('Feature Scatter Plots')
        pdf.add_image('reports/figures/feature_scatter_plots.png')




def select_features(data, method='correlation', threshold=0.4, pdf=None) -> pd.DataFrame:
    ''' Select features that have a correlation above a certain threshold with the target variable.

    Args:
        data (pd.DataFrame): The input DataFrame containing the data.
        method (str): The method to use for feature selection ('correlation' by default).
        threshold (float): The correlation threshold to determine if a feature is important.

    Returns:
        pd.DataFrame: A DataFrame with selected features above the correlation threshold.

    Description:
        This function calculates the correlation matrix, visualizes it, and selects features 
        based on their correlation with the target variable. It drops features with 
        correlation below the threshold and saves the cleaned data to a CSV file.
    '''

    print('+------------------------------------------------------------------------------------------------------------+')
    print('                                         -Select Features-')

    # Calculate the correlation matrix
    corr_matrix = data.corr()
    # Plot the correlation matrix
    fig, ax = plt.subplots(figsize=(VISUALIZATION_CONFIG['correlation_matrix_width'], VISUALIZATION_CONFIG['correlation_matrix_height']))
    # Visualize the correlation matrix
    cax = ax.matshow(corr_matrix, cmap=VISUALIZATION_CONFIG['correlation_matrix_cmap'])
    fig.colorbar(cax, shrink=VISUALIZATION_CONFIG['correlation_matrix_colorbar_shrink'])
    for i in range(corr_matrix.shape[0]):
        for j in range(corr_matrix.shape[1]):
            ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}', va='center', ha='center', color=VISUALIZATION_CONFIG['correlation_matrix_text_color'])
    ax.set_xticks(range(len(data.columns)))
    ax.set_yticks(range(len(data.columns)))
    ax.set_xticklabels(data.columns)
    ax.set_yticklabels(data.columns)
    ax.xaxis.set_ticks_position(VISUALIZATION_CONFIG['correlation_matrix_ticks_position'])
    plt.tight_layout()
    plt.savefig('reports/figures/correlation_matrix.png', dpi=VISUALIZATION_CONFIG['resolution'])

    # Select features with correlation above the threshold
    drop_features = []
    target = corr_matrix.index[-1]
    for feature in corr_matrix.index:
        if abs(corr_matrix.loc[feature, target]) < threshold:
            drop_features.append(feature)
    data = data.drop(drop_features, axis=1)
    print('Selected features based on correlation threshold.')
    print(f'Correlation threshold: {threshold}')
    print('Selected Features: ', data.columns.tolist())

    # Save the cleaned data
    data.to_csv('data/processed/data_select_features.csv', index=False)

    if pdf != None:
        pdf.add_page()
        pdf.chapter_sub_title('Select Features')
        pdf.chapter_body('Correlation Matrix')
        pdf.add_image('reports/figures/correlation_matrix.png')
        pdf.chapter_body('Select features based on correlation threshold.')
        pdf.chapter_body(f'Correlation threshold: {threshold}')
        pdf.chapter_body('Selected Features: '
                         f'{data.columns.tolist()}')

    return data
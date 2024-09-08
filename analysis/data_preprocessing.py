#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@Author: TZ
@Date: 2024/09/06 11:50
@Desc: This module provides functions for data cleaning, including handling missing values and outliers, 
       and functions for data transformation and normalization.
'''

from .config import VISUALIZATION_CONFIG
from .report_generation import PDF
from matplotlib import pyplot as plt
import pandas as pd


def remove_duplicates(data, pdf=None) -> pd.DataFrame:
    """Remove duplicate rows from the dataset.

    Args:
        data (pd.DataFrame): The input DataFrame containing the data.

    Returns:
        pd.DataFrame: A DataFrame with duplicate rows removed.

    Description:
        This function identifies and removes duplicate rows from the dataset. 
        It prints the number of duplicates found and saves the cleaned data to a CSV file.
    """

    print('+------------------------------------------------------------------------------------------------------------+')
    print('                                         -Remove Duplicates-')

    # Drop duplicates
    num_duplicates = data.duplicated().sum()
    print('Number of duplicate rows:', num_duplicates)
    data = data.drop_duplicates(keep='first', inplace=False)
    print('Duplicates removed.')

    # Save the cleaned data
    data.to_csv('data/processed/data_drop_duplicates.csv', index=False)

    # Generate PDF report
    if pdf != None:
        pdf.chapter_sub_title('Remove Duplicates')
        pdf.chapter_body(f'Number of duplicate rows: {num_duplicates}\n'
                         f'Duplicates removed.')

    return data


def handle_missing_values(data, method, group_by=None, pdf=None) -> pd.DataFrame:
    """Handle missing values in the dataset.

    Args:
        data (pd.DataFrame): The input DataFrame containing the data.
        method (str): The method to use for handling missing values ('drop', 'front', 'back', 'mean', 'median', 'group_mean', 'group_median').
        group_by (list, optional): A list of column names to group by for group mean or group median imputation.

    Returns:
        pd.DataFrame: A DataFrame with missing values handled according to the specified method.

    Description:
        This function detects and handles missing values in the dataset using various methods. 
        It supports dropping rows with missing values, filling them with previous/next row values, 
        column mean/median, or group mean/median based on the specified method. It also saves the cleaned data to a CSV file.
    """

    print('+------------------------------------------------------------------------------------------------------------+')
    print('                                         -Handle Missing Values-')

    # Detect missing values
    print('Rows with missing values:')
    missing_values = data[data.isnull().any(axis=1)]
    print(missing_values)
    percentage_missing_values = data.isnull().any(axis=1).sum() / data.shape[0] * 100
    percentage_missing_values = round(percentage_missing_values, 2)
    print(f'Percentage of rows with missing values: {percentage_missing_values}%')

    # If a row has at least 2 missing values, remove it
    data = data.dropna(thresh=2, axis=0, inplace=False)
    print('Rows with at least 2 missing values removed.')

    # Handle missing values
    if method == 'drop':
        # Drop rows with missing values
        data = data.dropna(axis=0, how='any', inplace=False)
        print('Rows with missing values removed.')
    elif method == 'front':
        # Fill missing values with the value in the previous row
        data = data.ffill(axis=0, inplace=False)
        print('Missing values filled with previous row values.')
    elif method == 'back':
        # Fill missing values with the value in the next row
        data = data.bfill(axis=0, inplace=False)
        print('Missing values filled with next row values.')
    elif method == 'mean':
        # Fill missing values with the mean of the column
        data = data.fillna(data.mean(), inplace=False)
        print('Missing values filled with column mean.')
    elif method == 'median':
        # Fill missing values with the median of the column
        data = data.fillna(data.median(), inplace=False)
        print('Missing values filled with column median.')
    elif method == 'group_mean':
        # Fill missing values with the mean of the group
        data = data.fillna(data.groupby(group_by).transform('mean'), inplace=False)
        print('Missing values filled with group mean.')
    elif method == 'group_median':
        # Fill missing values with the median of the group
        data = data.fillna(data.groupby(group_by).transform('median'), inplace=False)
        print('Missing values filled with group median.')
    else:
        pass

    # Save the cleaned data
    data.to_csv('data/processed/data_handle_missing_values.csv', index=False)

    # Generate PDF report
    if pdf != None:
        pdf.chapter_sub_title('Handle Missing Values')
        pdf.chapter_body(f'Rows with missing values:\n{missing_values}\n'
                         f'Percentage of rows with missing values:{percentage_missing_values.round(2)}%\n')
        pdf.chapter_body('Rows with at least 2 missing values removed.')
        pdf.chapter_body(f'Missing values handled using {method} method.')

    return data


def handle_outliers(data, method, negative_values=False, pdf=None) -> pd.DataFrame:
    """
    Handle outliers in the dataset.

    Args:
        data (pd.DataFrame): The input DataFrame containing the data.
        method (str): The method to use for handling outliers ('iqr').
        negative_values (bool): Flag to remove negative values from the dataset.

    Returns:
        pd.DataFrame: A DataFrame with outliers handled according to the specified method.

    Description:
        This function identifies and handles outliers in the dataset. 
        It supports removing negative values and outliers detected using the Interquartile Range (IQR) method. 
        It visualizes the data using boxplots and saves the cleaned data to a CSV file.
    """

    print('+------------------------------------------------------------------------------------------------------------+')
    print('                                         -Handle Outliers-')

    if negative_values:
        # Remove negative values
        data = data[data >= 0]
        print('Negative values removed.')
        pdf.chapter_body('Negative values removed.')

    if method == 'iqr':
        plt.figure(figsize=(VISUALIZATION_CONFIG['plot_width'], VISUALIZATION_CONFIG['plot_height']))
        data.boxplot(figsize=(VISUALIZATION_CONFIG['plot_width'], VISUALIZATION_CONFIG['plot_height']),
                     fontsize=VISUALIZATION_CONFIG['font_size'],
                     grid=True,
                     boxprops=VISUALIZATION_CONFIG['boxprops'],
                     whiskerprops=VISUALIZATION_CONFIG['whiskerprops'],
                     capprops=VISUALIZATION_CONFIG['capprops'],
                     medianprops=VISUALIZATION_CONFIG['medianprops'],
                     flierprops=VISUALIZATION_CONFIG['flierprops']
                     )
        plt.savefig('reports/figures/boxplot.png', dpi=VISUALIZATION_CONFIG['resolution'])        
        before = data.shape[0]

        # Calculate the unique values and their percentage
        unique_values = data.nunique()
        unique_values_percentage = unique_values / data.shape[0] * 100

        # Remove outliers using IQR method
        for column in data.columns:
            q1 = data[column].quantile(0.25)
            q3 = data[column].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            # Remove outliers if the unique values percentage is greater than 1 and the percentage of data within the bounds is greater than 97%
            if unique_values_percentage[column] > 1 and data.query(f'{lower_bound} <= {column} <= {upper_bound}').shape[0] / data.shape[0] > 0.97:
                data = data.query(f'{lower_bound} <= {column} <= {upper_bound}')
        print('Outliers removed using IQR method.')
        plt.figure(figsize=(VISUALIZATION_CONFIG['plot_width'], VISUALIZATION_CONFIG['plot_height']))
        data.boxplot(figsize=(VISUALIZATION_CONFIG['plot_width'], VISUALIZATION_CONFIG['plot_height']),
                     fontsize=VISUALIZATION_CONFIG['font_size'],
                     grid=True,
                     boxprops=VISUALIZATION_CONFIG['boxprops'],
                     whiskerprops=VISUALIZATION_CONFIG['whiskerprops'],
                     capprops=VISUALIZATION_CONFIG['capprops'],
                     medianprops=VISUALIZATION_CONFIG['medianprops'],
                     flierprops=VISUALIZATION_CONFIG['flierprops']                    
                     )
        plt.savefig('reports/figures/boxplot_cleaned.png', dpi=VISUALIZATION_CONFIG['resolution'])
        after = data.shape[0]

        print('Before:', before, 'After:', after)

    # Save the cleaned data
    data.to_csv('data/processed/data_handle_outliers.csv', index=False)

    if pdf != None:
        pdf.chapter_sub_title('Handle Outliers')
        if negative_values:
            pdf.chapter_body('Negative values removed.')
        if method == 'iqr':
            pdf.chapter_body('Outliers removed using IQR method.')
            pdf.add_page()
            pdf.chapter_body('Before:')
            pdf.add_image('reports/figures/boxplot.png')
            pdf.chapter_body('After:')
            pdf.add_image('reports/figures/boxplot_cleaned.png')


    return data
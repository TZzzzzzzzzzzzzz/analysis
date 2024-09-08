#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@Author: TZ
@Date: 2024/09/06 11:53
@Desc: This script evaluates the performance of various machine learning models by calculating different metrics based on the problem type. 
       It supports classification, regression, clustering, anomaly detection, dimensionality reduction, and reinforcement learning. 
       For regression, it also includes plotting of actual vs predicted values.
'''

import pandas as pd
from .config import VISUALIZATION_CONFIG
from .report_generation import PDF
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score, silhouette_score
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def evaluate_model(y_test, y_pred, problem_type, pdf=None) -> None:
    '''Evaluates the performance of a machine learning model based on the problem type.

    Args:
        y_test (array-like): True labels or values.
        y_pred (array-like): Predicted labels or values.
        problem_type (str): Type of the problem. Supported types are 'classification', 'regression', 'clustering', 'anomaly_detection', 'dimensionality_reduction', and 'reinforcement_learning'.
        pdf (PDF, optional): PDF object for generating a report. Default is None.

    Returns:
        None

    Raises:
        ValueError: If the problem type is unsupported.

    Description:
        This function prints the evaluation metrics and optionally adds them to a PDF report. 
        For regression problems, it also generates and saves scatter and line plots comparing actual and predicted values.
    '''
    
    print('+------------------------------------------------------------------------------------------------------------+')
    print('                                         -Evaluate Model-')
    
    if pdf != None:
        pdf.chapter_sub_title('Model Evaluation')

    if problem_type == 'classification':
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        print(f'Accuracy: {accuracy:.2f}')
        print(f'Precision: {precision:.2f}')
        print(f'Recall: {recall:.2f}')
        print(f'F1 Score: {f1:.2f}')
        if pdf != None:
            pdf.chapter_body(f'Accuracy: {accuracy:.2f}\nPrecision: {precision:.2f}\nRecall: {recall:.2f}\nF1 Score: {f1:.2f}')
    
    elif problem_type == 'regression':
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f'Mean Squared Error (MSE): {mse:.2f}')
        print(f'R^2 Score: {r2:.2f}')

        # Visualize the results by value
        plt.figure(figsize=(VISUALIZATION_CONFIG['plot_width'], VISUALIZATION_CONFIG['plot_height']))
        plt.scatter(y_test, y_pred, 
                    alpha=VISUALIZATION_CONFIG['scatter_alpha'],
                    color=VISUALIZATION_CONFIG['scatter_color'],
                    s=VISUALIZATION_CONFIG['scatter_size'],
                    marker=VISUALIZATION_CONFIG['scatter_marker'])
        min_val = min(min(y_test), min(y_pred))
        max_val = max(max(y_test), max(y_pred))
        plt.plot([min_val, max_val], [min_val, max_val], 
                 color=VISUALIZATION_CONFIG['scatter_line_color'], 
                 linestyle=VISUALIZATION_CONFIG['scatter_line_style'], 
                 linewidth=VISUALIZATION_CONFIG['scatter_line_width'])
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.grid(True)
        plt.title('Scatter plot for actual vs. predicted values')
        plt.savefig('reports/figures/model_evaluation_regression_scatter.png', dpi=VISUALIZATION_CONFIG['resolution'])

        # Visualize the results by index
        plt.figure(figsize=(VISUALIZATION_CONFIG['plot_width'], VISUALIZATION_CONFIG['plot_height']), 
                dpi=VISUALIZATION_CONFIG['resolution'])
        plt.plot(range(len(y_test)), y_test, 
                 color=VISUALIZATION_CONFIG['line_color1'], 
                 label='Actual', 
                 alpha=VISUALIZATION_CONFIG['line_alpha'],
                 linewidth=VISUALIZATION_CONFIG['line_width'],
                 marker=VISUALIZATION_CONFIG['line_marker'],
                 markersize=VISUALIZATION_CONFIG['line_marker_size'],
                 markerfacecolor=VISUALIZATION_CONFIG['line_marker_color1'],
                 linestyle=VISUALIZATION_CONFIG['line_style1'])
        plt.plot(range(len(y_pred)), y_pred, 
                 color=VISUALIZATION_CONFIG['line_color2'], 
                 label='Predicted', 
                 alpha=VISUALIZATION_CONFIG['line_alpha'],
                 linewidth=VISUALIZATION_CONFIG['line_width'],
                 marker=VISUALIZATION_CONFIG['line_marker'],
                 markersize=VISUALIZATION_CONFIG['line_marker_size'],
                 markerfacecolor=VISUALIZATION_CONFIG['line_marker_color2'],
                 linestyle=VISUALIZATION_CONFIG['line_style2'])
        plt.title('Line plot for actual vs. predicted values')
        plt.legend()
        plt.grid(True)
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.savefig('reports/figures/model_evaluation_regression_line.png', dpi=VISUALIZATION_CONFIG['resolution'])

        if pdf != None:
            pdf.chapter_body(f'Mean Squared Error (MSE): {mse:.2f}\nR^2 Score: {r2:.2f}')
            pdf.add_page()
            pdf.chapter_body('Scatter plot for actual vs. predicted values')
            pdf.add_image('reports/figures/model_evaluation_regression_scatter.png')
            pdf.chapter_body('Line plot for actual vs. predicted values')
            pdf.add_image('reports/figures/model_evaluation_regression_line.png')

    elif problem_type == 'clustering':
        silhouette_avg = silhouette_score(y_test, y_pred)
        print(f'Silhouette Score: {silhouette_avg:.2f}')
        if pdf != None:
            pdf.chapter_body(f'Silhouette Score: {silhouette_avg:.2f}')
    elif problem_type == 'anomaly_detection':
        # TODO: Add specific metrics for anomaly detection
        pass
    elif problem_type == 'dimensionality_reduction':
        # TODO: Add specific metrics for anomaly detection
        pass        
    elif problem_type == 'reinforcement__learning':
        # TODO: Add specific metrics for reinforcement learning
        pass
    else:
        raise ValueError(f"Unsupported problem type {problem_type}")
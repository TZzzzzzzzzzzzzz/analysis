#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@Author: TZ
@Date: 2024/09/06 11:52
@Desc: This script is designed to train various machine learning models based on the given dataset, problem type, and chosen algorithm.
       It supports classification, regression, clustering, anomaly detection, and dimensionality reduction tasks. 
       The script utilizes the scikit-learn library for model training and evaluation.
'''


import pandas as pd
from matplotlib import pyplot as plt
from .config import VISUALIZATION_CONFIG
from .config import MODEL_CONFIG
from .report_generation import PDF
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA


def train_model(data, problem_type, method, pdf=None) -> tuple:
    '''Train a machine learning model based on the specified problem type and method.
    
    Args:
        data (pd.DataFrame): The dataset containing features and target variable.
        problem_type (str): The type of machine learning problem (e.g., 'classification', 'regression').
        method (str): The specific method/algorithm to use for training (e.g., 'logistic_regression', 'linear_regression').
        pdf (PDF, optional): An optional PDF object for report generation.
    
    Returns:
        tuple: A tuple containing the true values and the predicted values for the test set.
    
    Description:
        This function trains a machine learning model based on the specified problem type and method. 
        It splits the data into training and testing sets, initializes the model, trains the model, 
        and makes predictions on the test set. 
        The function also generates a sub-chapter in the PDF report if provided.
    '''
    
    print('+------------------------------------------------------------------------------------------------------------+')
    print('                                         -Train Model-')
    
    # Split the data into features and target variable
    X = data[data.columns[:-1]]
    y = data[data.columns[-1]]
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                        test_size=MODEL_CONFIG['test_size'],
                                                        random_state=MODEL_CONFIG['random_state'])
    
    # Initialize the model based on the problem type and method
    if problem_type == 'classification':
        if method == 'logistic_regression':
            model = LogisticRegression()
        elif method == 'decision_tree':
            model = DecisionTreeClassifier()
        elif method == 'random_forest':
            model = RandomForestClassifier()
        else:
            raise ValueError(f"Unsupported method {method} for classification")
        
    elif problem_type == 'regression':
        if method == 'linear_regression':
            model = LinearRegression()
        elif method == 'decision_tree':
            model = DecisionTreeRegressor()
        elif method == 'random_forest':
            model = RandomForestRegressor()
        else:
            raise ValueError(f"Unsupported method {method} for regression")
        
    elif problem_type == 'clustering':
        if method == 'kmeans':
            model = KMeans(n_clusters=MODEL_CONFIG['n_clusters'])
        else:
            raise ValueError(f"Unsupported method {method} for clustering")
        
    elif problem_type == 'anomaly_detection':
        if method == 'isolation_forest':
            model = IsolationForest()
        else:
            raise ValueError(f"Unsupported method {method} for anomaly detection")
        
    elif problem_type == 'dimensionality_reduction':
        if method == 'pca':
            model = PCA(n_components=MODEL_CONFIG['n_components'])
        else:
            raise ValueError(f"Unsupported method {method} for dimensionality reduction")
        
    elif problem_type == 'reinforcement_learning':
        raise NotImplementedError("Reinforcement learning is not implemented yet")
    
    else:
        raise ValueError(f"Unsupported problem type {problem_type}")

    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = model.predict(X_test)

    print('Training data size:', X_train.shape[0], 'samples.')
    print('Testing data size:', X_test.shape[0], 'samples.')
    print('Problem Type:', problem_type)
    print('Method:', method)
    print('Model:', model)
    print('Training completed successfully.')

    # Generate PDF report
    if pdf != None:
        pdf.chapter_sub_title(f'Train Model')
        pdf.chapter_body(f'Training data size: {X_train.shape[0]} samples.')
        pdf.chapter_body(f'Testing data size: {X_test.shape[0]} samples.')
        pdf.chapter_body(f'Problem Type: {problem_type}')
        pdf.chapter_body(f'Method: {method}')
        pdf.chapter_body(f'Model: {model}')

    return y_test, y_pred
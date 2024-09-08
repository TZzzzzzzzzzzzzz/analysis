#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@Author: TZ
@Date: 2024/09/06 11:51
@Desc: This module performs Exploratory Data Analysis (EDA), including statistical analysis and visualization.
'''

from .report_generation import PDF
import pandas as pd


def summary_statistics(data, pdf=None) -> None:
    """Generate summary statistics for the dataset.

    This function prints various statistical insights about the dataset, 
    including data size, basic information, random sample, and descriptive statistics.

    Args:
        data (pd.DataFrame): The pandas DataFrame for which to generate statistics.

    Returns:
        None: This function does not return any value but prints the statistics directly.
    """
    
    print('+------------------------------------------------------------------------------------------------------------+')
    print("                                         -Data Size-")

    print("Total number of entries:", data.shape[0])
    print("Total number of columns:", data.shape[1])
    print("Total number of data points:", data.size)
    print("Total number of missing values: ", data.isnull().sum().sum())
    print("Percentage of missing values: ", ((data.isnull().sum().sum() / data.size) * 100).round(2))
    print("Percentage of missing values in each column:")
    print(data.isnull().sum() / data.shape[0] * 100)

    print('+------------------------------------------------------------------------------------------------------------+')
    print('                                         -Data Basic Information-')
    info = data.info()

    print('+------------------------------------------------------------------------------------------------------------+')
    print('                                         -Random Sample of Data-')
    sample = data.sample(5).round(2)
    print(sample)
    
    print('+------------------------------------------------------------------------------------------------------------+')
    print('                                         -Data Statistics-')
    description = data.describe().round(2)
    print(description)
    
    # Generate PDF report
    if pdf != None:
        pdf.chapter_sub_title('Data Size')
        pdf.chapter_body(f'Total number of entries: {data.shape[0]}\n'
                         f'Total number of columns: {data.shape[1]}\n'
                         f'Total number of data points: {data.size}\n'
                         f'Total number of missing values: {data.isnull().sum().sum()}\n'
                         f'Percentage of missing values: {(data.isnull().sum().sum() / data.size) * 100}')
        pdf.chapter_sub_title('Random Sample of Data')
        pdf.chapter_body(f'{sample}')
        pdf.chapter_sub_title('Data Statistics')
        pdf.chapter_body(f'{description}')
    
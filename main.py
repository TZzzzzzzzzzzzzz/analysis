#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@Author: TZ
@Date: 2024/09/06 11:14
@Desc: This script is designed to analyze the Boston Housing dataset using machine learning.
'''


from analysis import config
from analysis import data_loading
from analysis import data_exploration
from analysis import data_preprocessing
from analysis import feature_engineering
from analysis import model_building
from analysis import evaluation
from analysis import report_generation
import logging
import time


# Set up logging
logging.basicConfig(
    level=config.LOGGING_CONFIG['log_level'],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=config.LOGGING_CONFIG['log_file_path'],
)

def main():
    # Start the timer
    start_time = time.time()

    # Create a PDF object
    pdf = report_generation.PDF()
    pdf.cover_page('Boston Housing', 'ZHAO Cheng', '2024/09/06')

    # Load data
    data = data_loading.load_data('csv')
    
    # Explore the data
    pdf.add_page()
    pdf.chapter_title('Data Exploration')
    data_exploration.summary_statistics(data, pdf)
    
    
    # Perform data preprocessing
    pdf.add_page()
    pdf.chapter_title('Data Preprocessing')
    data = data_preprocessing.remove_duplicates(data, pdf=pdf)
    data = data_preprocessing.handle_missing_values(data, method='front', pdf=pdf)
    data = data_preprocessing.handle_outliers(data, method='iqr', negative_values=True, pdf=pdf)
    
    # Perform feature engineering
    pdf.add_page()
    pdf.chapter_title('Feature Engineering')
    feature_list = ['INDUS', 'RM', 'TAX', 'LSTAT', 'MEDV']
    feature_engineering.visualize_features(data, feature_list, pdf=pdf)
    data = feature_engineering.select_features(data, method='correlation', threshold=0.4, pdf=pdf)

    # Build and evaluate a machine learning model
    pdf.add_page()
    pdf.chapter_title('Model Building and Evaluation')
    y_test, y_pred = model_building.train_model(data, problem_type='regression', method='decision_tree', pdf=pdf)
    evaluation.evaluate_model(y_test, y_pred, problem_type='regression', pdf=pdf)
    
    # Save PDF reports
    pdf.save_pdf()
    
    # Log the completion of the analysis
    print('Analysis completed successfully.')

    # Stop the timer
    end_time = time.time()

    # Log the time elapsed
    print('Time elapsed:', end_time - start_time, 'seconds.')

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@Author: TZ
@Date: 2024/09/06 10:56
@Desc: This script is designed to handle data processing and analysis tasks. 
       It includes configurations for data file paths, API keys, analysis parameters, 
       logging, and visualization settings.
'''


import os


# Configuration for data file paths
DATA_PATH = {
    'raw': 'data/raw/',
    'processed': 'data/processed/',
}

# Specific data file paths
CSV_FILE_PATH = os.path.join(DATA_PATH['raw'], 'housing_data_raw.csv')
EXCEL_FILE_PATH = os.path.join(DATA_PATH['raw'], 'sample.xlsx')

# API keys (if the project needs to use external APIs)
API_KEYS = {
    'api_key': 'YOUR_API_KEY_HERE',
}

# Parameters that might be needed during the analysis process
ANALYSIS_CONFIG = {
    'parameter1': 'value1',
    'parameter2': 'value2',
}

# Logging configuration
LOGGING_CONFIG = {
    'log_file_path': 'logs/analysis.log',
    'log_level': 'DEBUG',
}

# Visualization configuration
VISUALIZATION_CONFIG = {
    'plot_width': 21,
    'plot_height': 9,
    'plot_width_subplots': 15,
    'plot_height_subplots': 12,

    'resolution': 150,
    'font_size': 12,
    'font': 'Arial',
    'background_color': '#ffffff',
    'title_font_size': 16,
    'title_font': 'Helvetica',
    'title_color': '#000000',
    'title_alpha': 1.0,
    'axis_label_font_size': 14,
    'axis_label_font': 'Verdana',
    'axis_label_color': '#333333',
    'axis_label_alpha': 1.0,
    'legend_font_size': 12,
    'legend_font': 'Times New Roman',
    'legend_color': '#555555',
    'legend_alpha': 1.0,
    'grid_line_color': '#dddddd',
    'grid_line_width': 1,
    'grid_line_alpha': 0.5,
    'plot_border_color': '#aaaaaa',
    'plot_border_width': 1,
    'plot_border_alpha': 1.0,
    'tooltip_font_size': 10,
    'tooltip_font': 'Courier New',
    'tooltip_color': '#ffffff',
    'tooltip_alpha': 0.9,
    'marker_size': 6,
    'marker_alpha': 0.8,
    'line_width': 2,
    'line_alpha': 0.8,
    'bar_alpha': 0.7,

    'boxprops': dict(linestyle='-', linewidth=3, color='blue', alpha=0.7), # Box properties
    'whiskerprops': dict(linestyle='-', linewidth=2, color='blue', alpha=0.7),
    'capprops': dict(linestyle='-', linewidth=2, color='blue', alpha=0.7),
    'medianprops': dict(linestyle='-', linewidth=3, color='red', alpha=0.7),
    'flierprops': dict(marker='o', markerfacecolor='black', markersize=7, linestyle='none', alpha=0.2), 
    
    'hist_bins': 40,
    'hist_color': 'skyblue',
    'hist_alpha': 0.7,
    'hist_edgecolor': 'black',
    

    
    'correlation_matrix_width': 16,
    'correlation_matrix_height': 16,
    'correlation_matrix_cmap': 'coolwarm',
    'correlation_matrix_text_color': 'black',
    'correlation_matrix_colorbar_shrink': 0.6,
    'correlation_matrix_ticks_position': 'bottom',
    
    'scatter_alpha': 0.7,
    'scatter_color': 'blue',
    'scatter_size': 50,
    'scatter_marker': '.',
    'scatter_line_color': 'red',
    'scatter_line_style': '--',
    'scatter_line_width': 2,
    
    'line_color1': 'red',
    'line_color2': 'blue',
    'line_marker_color1': 'red',
    'line_marker_color2': 'blue',
    'line_alpha': 0.7,
    'line_width': 2,
    'line_marker': '.',
    'line_marker_size': 10,
    'line_style1': '-',
    'line_style2': '--',
}

# Model configuration
MODEL_CONFIG = {
    'test_size': 0.2,
    'random_state': 42,
    'n_clusters': 3,
    'n_components': 2,
}
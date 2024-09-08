#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@Author: TZ
@Date: 2024/09/06 11:36
@Desc: This module provides a function to load data from specified document types.
'''

from .config import CSV_FILE_PATH, EXCEL_FILE_PATH
import pandas as pd

def load_data(doc_type: str) -> pd.DataFrame:
    """Load data from a specified document type (CSV or Excel).

    Args:
        doc_type (str): The type of the document to load, either 'csv' or 'excel'.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.

    Raises:
        ValueError: If an invalid document type is provided.
    """
    # Load data based on the document type
    if doc_type == 'csv':
        return pd.read_csv(CSV_FILE_PATH)
    elif doc_type == 'excel':
        return pd.read_excel(EXCEL_FILE_PATH)
    else:
        raise ValueError('Invalid document type. Please provide either "csv" or "excel".')
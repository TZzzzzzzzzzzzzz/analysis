# Crawler, Data Analysis and Machine Learning Project

## Overview

This project can automatically crawl data from web pages and store it in CSV or Excel format. 
After the raw data is crawled (or provided), the project is designed to handle various data processing and analysis tasks, including data loading, preprocessing, exploratory data analysis (EDA), feature engineering.
Then the project can conduct model building, evaluation, and PDF report generation. 
The project is structured into multiple modules, each responsible for a specific aspect of the data analysis pipeline.

## Project Structure

- `config.py`: Contains configuration settings for data file paths, API keys, analysis parameters, logging, and visualization settings.
- `data_loading.py`: Provides functions to load data from specified document types (CSV or Excel).
- `data_exploration.py`: Performs Exploratory Data Analysis (EDA), including statistical analysis and visualization.
- `data_preprocessing.py`: Contains functions for data cleaning, including handling missing values and outliers, and data transformation and normalization.
- `feature_engineering.py`: Contains functions for creating new features, modifying existing features, and selecting important features to improve model performance.
- `model_building.py`: Trains various machine learning models based on the given dataset, problem type, and chosen algorithm.
- `evaluation.py`: Evaluates the performance of various machine learning models by calculating different metrics based on the problem type.
- `report_generation.py`: Generates an analysis report in PDF format using the FPDF library.
- `main.py`: The main script that orchestrates the entire data analysis pipeline.
- `bilibili.py`: Scrapes video information from Bilibili using Selenium.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/TZzzzzzzzzzzzzz/analysis.git
    cd analysis
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages listed in the `requirements.txt` file:
    ```sh
    pip install -r requirements.txt
    ```


## Usage

1. **Configuration**: Update the `config.py` file with the appropriate paths, API keys, and other configuration settings.

2. **Scrape Bilibili Videos**: Execute the `bilibili.py` script to scrape video information from Bilibili:
    ```sh
    python bilibili.py
    ```

3. **Run the Main Script**: Execute the `main.py` script to run the entire data analysis pipeline:
    ```sh
    python main.py
    ```

## Modules

### config.py
Contains configuration settings for data file paths, API keys, analysis parameters, logging, and visualization settings.

### bilibili.py
Scrapes video information from Bilibili using Selenium.

### data_loading.py
Provides functions to load data from specified document types (CSV or Excel).

### data_exploration.py
Performs Exploratory Data Analysis (EDA), including statistical analysis and visualization.

### data_preprocessing.py
Contains functions for data cleaning, including handling missing values and outliers, and data transformation and normalization.

### feature_engineering.py
Contains functions for creating new features, modifying existing features, and selecting important features to improve model performance.

### model_building.py
Trains various machine learning models based on the given dataset, problem type, and chosen algorithm.

### evaluation.py
Evaluates the performance of various machine learning models by calculating different metrics based on the problem type.

### report_generation.py
Generates an analysis report in PDF format using the FPDF library.

### main.py
The main script that orchestrates the entire data analysis pipeline.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Pandas](https://pandas.pydata.org/)
- [Scikit-learn](https://scikit-learn.org/)
- [FPDF](http://www.fpdf.org/)
- [Selenium](https://www.selenium.dev/)
- [Matplotlib](https://matplotlib.org/)

## Author

ZHAO Cheng

## Contact

For any inquiries, please contact ZHAO Cheng at [c-zhao23@mails.tsinghua.edu.cn](mailto:c-zhao23@mails.tsinghua.edu.cn).
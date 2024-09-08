#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@Author: TZ
@Date: 2024/09/08 16:24
@Desc: This script is designed to scrape video information from Bilibili using Selenium.
'''

import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class Bilibili:
    def __init__(self):
        self.url = 'https://www.bilibili.com/' 
        self.service = EdgeService(EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(service=self.service)

    def get(self):
        self.driver.get(self.url)

    def close(self):
        self.driver.quit()

    def get_video_info(self, keyword) -> pd.DataFrame:
        # Initialize lists to store video information
        titles = []
        authors = []
        dates = []
        video_info = {'Title': titles, 'Author': authors, 'Dates': dates}

        # Search for videos by keyword
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div/div/form/div[1]/input")))
        self.key = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div/div/form/div[1]/input")
        self.key.send_keys(keyword)
        self.button = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div/div/form/div[2]")
        self.button.click()

        # Switch to the search results page
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[1])
        time.sleep(1)

        # Get the number of pages
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[4]/div/div/button[9]")))
            self.button = self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[4]/div/div/button[9]")
            self.button_text = self.button.text
            self.number = re.findall(r'\d+', self.button_text)[0]
        except Exception:
            # Default to 1 page if page number is not found
            self.number = 1

        # Get video information from the first page
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "bili-video-card__info--tit")))
            video_cards = self.driver.find_elements(By.CLASS_NAME, "bili-video-card")
        except TimeoutException:
            # Set video_cards to an empty list if there's a timeout
            video_cards = []

        for card in video_cards:
            titles.append(card.find_element(By.CLASS_NAME, "bili-video-card__info--tit").text if card.find_elements(By.CLASS_NAME, "bili-video-card__info--tit") else None)
            authors.append(card.find_element(By.CLASS_NAME, "bili-video-card__info--author").text if card.find_elements(By.CLASS_NAME, "bili-video-card__info--author") else None)
            dates.append(card.find_element(By.CLASS_NAME, "bili-video-card__info--date").text if card.find_elements(By.CLASS_NAME, "bili-video-card__info--date") else None)

        # Navigate to subsequent pages
        self.button = self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[4]/div/div/button[10]")
        self.button.click()

        # Continue scraping until the last page
        i = 2
        while i <= int(self.number):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            try:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "bili-video-card__info--tit")))
                video_cards = self.driver.find_elements(By.CLASS_NAME, "bili-video-card")
            except TimeoutException:
                # Set video_cards to an empty list if there's a timeout
                video_cards = []

            for card in video_cards:
                titles.append(card.find_element(By.CLASS_NAME, "bili-video-card__info--tit").text if card.find_elements(By.CLASS_NAME, "bili-video-card__info--tit") else None)
                authors.append(card.find_element(By.CLASS_NAME, "bili-video-card__info--author").text if card.find_elements(By.CLASS_NAME, "bili-video-card__info--author") else None)
                dates.append(card.find_element(By.CLASS_NAME, "bili-video-card__info--date").text if card.find_elements(By.CLASS_NAME, "bili-video-card__info--date") else None)

            if i < 6 or i >= int(self.number) - 4:
                self.button = self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[2]/div/div/div[2]/div/div/button[10]")
                self.button.click()
            elif i >= 6:
                self.button = self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[2]/div/div/div[2]/div/div/button[9]")
                self.button.click()
            i += 1

        data = pd.DataFrame(video_info)
        return data


if __name__ == '__main__':
    bilibili = Bilibili()
    bilibili.get()
    data = bilibili.get_video_info(keyword='python')
    
    # Save as a CSV file
    data.to_csv('data/raw/bilibili_videos.csv', index=False)
    bilibili.close()
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@Author: TZ
@Date: 2024/09/06 11:53
@Desc: This module generates an analysis report in PDF format using the FPDF library.
'''

from fpdf import FPDF
from PIL import Image

class PDF(FPDF):
    """A specialized FPDF class for generating PDF reports with custom headers, footers,
    and content layout.
    """
    
    def __init__(self):
        """Initializes the PDF object, sets up page breaking, and adds the first page.
        """
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Data Analysis Report', 0, 1, 'C')
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def cover_page(self, title, author, date):
        """Adds a cover page to the PDF report.
        
        Args:
            title (str): The title of the report.
            author (str): The author of the report.
            date (str): The date of the report.
        """
        self.set_font('Arial', 'B', 24)
        page_height = self.h
        self.set_y(page_height / 2 - 20)
        self.cell(0, 10, title, 0, 1, 'C')
        self.ln(10)
        self.set_font('Arial', 'I', 14)
        self.cell(0, 10, f'Author: {author}', 0, 1, 'C')
        self.cell(0, 10, f'Date: {date}', 0, 1, 'C')

    def add_heading(self, title, level=1):
        """Adds a heading to the PDF with optional heading level.
        
        Args:
            title (str): The text for the heading.
            level (int): The heading level (default is 1).
        """
        font_size = 16 if level == 1 else 14
        self.set_font('Arial', 'B', font_size)
        self.cell(0, 10, title, 0, 1, 'L')

    def chapter_title(self, title):
        """Adds a chapter title to the PDF.
        
        Args:
            title (str): The text for the chapter title.
        """
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, title, 0, 1, 'L')
    
    def chapter_sub_title(self, title):
        """Adds a chapter sub-title to the PDF.
        
        Args:
            title (str): The text for the chapter sub-title.
        """
        self.set_font('Arial', 'B', 8)
        self.cell(0, 10, title, 0, 1, 'L')

    def chapter_body(self, body):
        """Adds body text to the current chapter in the PDF.
        
        Args:
            body (str): The text for the chapter body.
        """
        self.set_font('Times', '', 8)
        self.multi_cell(0, 10, body)
        #self.ln(0.5)

    def add_chapter(self, title, body):
        """Adds a new chapter to the PDF with a title and body text.
        
        Args:
            title (str): The title of the chapter.
            body (str): The main content of the chapter.
        """
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(body)

    def get_image_size(self, image_path):
        """Retrieves the size of an image to scale it appropriately for the PDF layout.
        
        Args:
            image_path (str): The file path to the image.
        
        Returns:
            tuple: A tuple containing the width and height of the image.
        """
        with Image.open(image_path) as img:
            return img.width, img.height

    def add_image(self, image_path):
        """Adds an image to the PDF, scaling and centering it on the page.
        
        Args:
            image_path (str): The file path to the image to be added.
        """
        img_width, img_height = self.get_image_size(image_path)
        img_width, img_height = img_width / 15, img_height / 15
        x = (self.w - img_width) / 2
        y = self.get_y()
        self.image(image_path, x, y, img_width, img_height)
        self.ln(img_height)

    def save_pdf(self, file_path='reports/pdf_reports/pdf_report.pdf'):
        """Saves the PDF report to a file.
        
        Args:
            file_path (str): The path where the PDF report will be saved.
        """
        self.output(file_path)
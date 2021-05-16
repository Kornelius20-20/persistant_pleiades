"""

Author: Janith Weeraman
Date: 27/04/2021

A script to pull the abstracts from the page url
"""

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os


class GetAbstract:
    driver = None  # Variable to hold the HTMLSession object

    def __init__(self):
        self.driver = HTMLSession()

    def getAbstract(self, url) -> str:
        # Make the webdriver the active webdriver created at init
        driver = self.driver
        paras = None  # Variable to hold abstract paragraph

        # Get URL and extract page source to make soup with
        driver = driver.get(url)
        page = driver.html.html
        soup = BeautifulSoup(page, 'html.parser')

        # Find the abstract title and search for the paragraph tag corresponding
        # to the abstract
        headings = ['Abstract', 'ABSTRACT', 'Summary', 'SUMMARY']

        for text in headings:
            outer = False  # to break out of outer loop
            # For each possible text in headings find if there are any paragraphs under it
            abs = soup.find_all(text=text)

            for tag in abs:

                tag = tag.find_parent()  # Find the current tag name
                if tag.name not in ('span', 'a'):  # These tags tend to give false results
                    # Find a relavant paragraph that hopefully has the abstract
                    paras = tag.find_parent().find('p')

                if paras is not None:
                    outer = True
                    break

            if outer:
                break

        if paras is not None:
            return paras.text
        else:
            return "N/A Could not find An abstract"


if __name__ == '__main__':
    # Test url
    url = "https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1348-0421.2001.tb02614.x"
    abs = GetAbstract()
    print(abs.getAbstract(url))

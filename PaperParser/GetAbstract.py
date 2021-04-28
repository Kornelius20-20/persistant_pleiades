"""

Author: Janith Weeraman
Date: 27/04/2021

A script to pull the abstracts from the page url
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os

class GetAbstract:
    driver = None # Variable to hold the webdriver

    def __init__(self):
        try:
            # Create Webdriver
            # Options for a headless webdriver
            from selenium.webdriver.firefox.options import Options as OptionsFirefox

            options = OptionsFirefox()
            options.add_argument('--headless')
            driverpath = os.path.join(os.getcwd(), "webdriver\\geckodriver.exe")

            self.driver = webdriver.Firefox(executable_path=driverpath, options=options)

        except WebDriverException:

            # If there is no firefox browser installed then try to form a chrome webdriver
            from selenium.webdriver.chrome.options import Options as OptionsChrome

            options = OptionsChrome()
            options.add_argument('--headless')
            driverpath = os.path.join(os.getcwd(), "webdriver\\chromedriver.exe")

            try:
                self.driver = webdriver.Chrome(executable_path=driverpath,options=options)
            except WebDriverException:

                # Raise an error if neither browser is present
                raise WebDriverException("There are no compatible browsers installed. Please"
                                         "install either Firefox or Chrome")

    def getAbstract(self,url) -> str:
        # Make the webdriver the active webdriver created at init
        driver = self.driver
        paras = None  # Variable to hold abstract paragraph

        # Get URL and extract page source to make soup with
        driver.get(url)
        page = driver.page_source
        soup = BeautifulSoup(page,'html.parser')

        # Find the abstract title and search for the paragraph tag corresponding
        # to the abstract
        abs = soup.find_all(text='Abstract')
        for tag in abs:
            tag = tag.find_parent()
            if tag.name != 'span':
                paras = tag.find_parent().find('p')

        if paras is not None:
            return paras.text
        else:
            return "N/A Could not find An abstract"

    def driver_quit(self) -> None:
        self.driver.quit()

if __name__ == '__main__':
    # Test url
    url = "https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1348-0421.2001.tb02614.x"
    abs = GetAbstract()
    print(abs.getAbstract(url))
    abs.driver_quit()
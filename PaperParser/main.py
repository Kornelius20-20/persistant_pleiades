"""

Author: Janith Weeraman
Date: 27/04/2021

A python console app that uses scholarly to access academic paperss via google scholar

"""

import subprocess,sys
from GetAbstract import GetAbstract
import pip

version = '1.0'
packages = set('scholarly','selenium')

def _check_req(package):
    """
    Method to Check to see if scholarly is installed and if not try to install it
    """
    # Get installed packages and put them into a list
    reqs = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

    # Check list for scholarly and attempt to install if not in it
    if package not in installed_packages:
        # subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        pip.main(['install', package])

# Testing
keywords = "Primate Hox"

def get_paper_info(keywords,num_results = 20):

    from scholarly import scholarly
    # Search based on keywords and return a list of results
    search_query = scholarly.search_pubs(keywords)

    # Create a new webdriver from GetAbstracts to get the abstract files fully
    abstract = GetAbstract()

    for num in range(num_results):
        query = next(search_query)
        abs = abstract.getAbstract(query['pub_url'])
        print(f'{num+1}) title:\n ',query['bib']['title'])
        print('Abstract:\n ', abs)
        print('url:\n ', query['pub_url'])
        print('\n')

    # Close webdriver
    abstract.driver_quit()

def intro():
    print(f'\t\twelcome to paper parser version {version}!')
    print(f'\t\t written by Janith Weeraman.\n')

    mode = input("Please enter the keywords you wish to search for:")
    results = int(input("How many results should I show?"))

    print('\n')

    return [mode,results]

if __name__ == '__main__':
    for package in packages:
        _check_req(package)
    keywords = intro()
    get_paper_info(keywords[0],keywords[1])
    input()
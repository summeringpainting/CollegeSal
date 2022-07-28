from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from lxml import etree
import os
os.chdir("/home/steve/Python/BS4")

# Get page and make it into soup
URL = "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors"
def scraper(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Use panda to do most of the table scraping, other headers need to be
    # scraped differently
    dfs = pd.read_html(URL)
    df = dfs[0]
    df2 = df[['Rank', 'Major', 'Degree Type']]

    # Make list of all table values
    list_of_values = soup.find_all(class_="data-table__value")

    # Make list for early career sallarys by getting every 4th value
    early_sal = list_of_values[0::3]

    # Clean list to append to
    early_sal_list = []

    # iterate through list taking out text and then stepping through it to take
    # out correct values
    for i in early_sal:
        early_sal_list.append(i.text)

    # Add list to DataFrame
    df2['Early Career Pay'] = early_sal_list[1::2]

    # Get values from checking for "$" and getting every other list item
    midcareer = []
    for i in list_of_values:
        if "$" in i.text:
            midcareer.append(i.text)

    # Add list to DataFrame
    df2['Mid Career Pay'] = midcareer[1::2]

    # Create list for % High Meaning
    meany = []
    for i in list_of_values:
        if i.text == "-" or re.search(r'%', i.text):
            meany.append(i.text)

    print(f"{meany} is meany")
    # Add High Meaning column to DataFrame
    df2['% High Meaning'] = meany
    return df2


scraper(URL).to_csv('collegesal3.csv')

for i in range(2, 35):
    URL = f"https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/{i}"
    scraper(URL).to_csv('collegesal3.csv', mode='a')

# last page
# URL = f"https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/34"
# page = requests.get(URL)
# soup = BeautifulSoup(page.content, 'html.parser')

# dfs = pd.read_html(URL)
# df = dfs[0]
# df2 = df[['Rank', 'Major', 'Degree Type']]

# # Make list of all table values
# list_of_values = soup.find_all(class_="data-table__value")

# # Make list for early career sallarys by getting every 4th value
# early_sal = list_of_values[0::3]

# # Clean list to append to
# early_sal_list = []

# # iterate through list taking out text and then stepping through it to take
# # out correct values
# for i in early_sal:
#     early_sal_list.append(i.text)

# # Add list to DataFrame
# df2['Early Career Pay'] = early_sal_list[1::2]

# # Get values from checking for "$" and getting every other list item
# midcareer = []
# for i in list_of_values:
#     if "$" in i.text:
#         midcareer.append(i.text)

# # Add list to DataFrame
# df2['Mid Career Pay'] = midcareer[1::2]

# # Create list for % High Meaning
# meany = []
# for i in list_of_values:
#     if re.search(r'-', i.text) or re.search(r'%', i.text):
#         meany.append(i.text)

# # Add High Meaning column to DataFrame
# df2['% High Meaning'] = meany

# print(df2)

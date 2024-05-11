# Importing the libraries
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os

# Read the input file using pandas
inputs = pd.read_excel('../Files/Input.xlsx')

# Create a folder to save the articles
def create_articles():
    curr_dir = os.getcwd()
    articles = 'articles'
    path = os.path.join(curr_dir, articles)

    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print(f"Directory {path} already exists")


# Define a function to web scrape the data
def scraping(dataframe):

    # Make a pandas df to save all article in a df for NLP
    df = pd.DataFrame(columns=['URL_ID', 'text'])

    # Using a dataframe iter rows to loop through all the links and send get requests to the page
    for index, row in dataframe.iterrows():
        article = row['URL']
        page = requests.get(article)

        # Print URL_ID to see the current article being scraped
        print(row['URL_ID'])

        # Extracting the heading and body of the articles
        if page.status_code == 200:     # If page is found
            pageSoup = BeautifulSoup(page.content, features='lxml')

            # Introducing a try and except block to handle different selectors for heading and body
            try:
                title = pageSoup.find('h1', {'class': 'entry-title'}).text.strip()
                body = pageSoup.find('div', {'class': 'td-post-content tagdiv-type'}).text.strip()
            except AttributeError:
                title = pageSoup.find('h1', {'class': 'tdb-title-text'}).text.strip()
                body = pageSoup.find_all('div', {'class': 'tdb-block-inner td-fix-index'})[14].text.strip()

            # Append data into the df
            new_row = pd.DataFrame({'URL_ID': [row['URL_ID']], 'text': [f"{title} {body}"]})

            # Concatenate the new DataFrame with the existing one
            df = pd.concat([df, new_row], ignore_index=True)

            # Check if the file already exists
            file_path = f"articles/{row['URL_ID']}.txt"

            # If the file doesn't exist, create and write to it
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:       # ignore characters that cannot be encoded or decoded with utf-8
                    file.write(f"{title} \n\n{body} \n")
            else:
                print(f"File '{row['URL_ID']}' already exists")

        # Continue to next url if page not found
        else:
            continue

    # Save the dataframe from NLP
    with open("combined.csv", 'w', encoding='utf-8', errors='ignore') as file:
        file.write(df.to_csv(index=False))


if __name__ == "__main__":
    create_articles()
    scraping(inputs)

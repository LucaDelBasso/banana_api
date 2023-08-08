import requests, re, os
from requests.adapters import HTTPAdapter, Retry
import csv
import json
from datetime import datetime
from bs4 import BeautifulSoup

BASE_URL = 'https://www.gov.uk'
GOV_URL = f'{BASE_URL}/government/statistical-data-sets/banana-prices'

USER = os.getenv("SCRAPER_POST_USERNAME", "")
PASS = os.getenv("SCRAPER_POST_PASSWORD", "")


def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    r.close()
    return soup

#'https://www.gov.uk/government/statistical-data-sets/banana-prices'

def get_url(all_data=False):
    soup = get_soup(GOV_URL)

    if all_data:
        section = soup.find_all('h2', {'class' : 'gem-c-attachment__title'})[2]
    else:
        section = soup.find_all('p', {'class': 'gem-c-attachment__metadata'})[5]
    
    url = section.find('a', {'class': 'govuk-link'})['href']
    return url

def get_all_bananas():
    csv_url = get_url(all_data=True)
    csv_response = requests.get(csv_url)
    return csv_response

def get_newest_bananas(last_date_in_db):

    relative_url = get_url(all_data=False)
    
    preview_url = f'{BASE_URL}{relative_url}'
    soup = get_soup(preview_url)
    table_body = soup.find('tbody')
    rows = table_body.find_all('tr')

    array = []
    for row in rows:
        cells = row.getText().split('\n')[1:-1]
        date_in_row = datetime.strptime(cells[1], '%Y-%m-%d')

        if date_in_row <= last_date_in_db:
            break

        cleaned_data_row = {
            'origin': cells[0],
            'date': cells[1],
            'price': cells[2],
            'units': cells[3]
        }
        array.append(cleaned_data_row)

    return array

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

response = get_all_bananas()
reader = csv.reader(response.text.split('\n'), delimiter=',')
next(reader, None) #ignore header


for row in reader:
    if row:
        json_data = {
            'origin': row[0],
            'publication_date': str(datetime.strptime(row[1], '%Y-%m-%d')),
            'price': float(row[2]),
            'units': row[3]
            }
        
        url = 'http://banana-api/bananas/'

        response = requests.post(url, headers=headers,
                                 json=json_data, auth=(USER, PASS))
        
        print(response.status_code)
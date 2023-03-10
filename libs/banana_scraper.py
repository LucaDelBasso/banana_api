import requests, re
import json
from pyexcel_ods3 import read_data
from datetime import datetime
from bs4 import BeautifulSoup

BASE_URL = 'https://www.gov.uk'
GOV_URL = f'{BASE_URL}/government/statistical-data-sets/banana-prices'

def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    r.close()
    return soup

def get_url(span_class='preview'):
    soup = get_soup(GOV_URL)
    span = soup.find('span', {'class' : span_class})
    url = span.find('a', {'class': 'govuk-link'})['href']
    return url

def get_all_bananas():
    csv_url = get_url(span_class='download')
    csv_response = requests.get(csv_url)
    return csv_response

def get_newest_bananas(last_date_in_db):

    relative_url = get_url(span_class='preview')
    
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
            'units': cells[3],
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        array.append(cleaned_data_row)

    return array

# get_newest_bananas(datetime(2022, 12, 9))
get_all_bananas()
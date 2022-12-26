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

def get_all_bananas():
    response = requests.get(GOV_URL)
    csv_url = re.search(r'https:\/\/.+\/bananas-.+csv', response.text)[0]
    csv_response = requests.get(csv_url)
    return csv_response

def get_newest_bananas(last_date_in_db):
    soup = get_soup(GOV_URL)
    relative_url = soup.find('a', {'class': 'govuk-link', 'href': re.compile('/preview')})['href']
    
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
            'country': cells[0],
            'date': cells[1],
            'price': cells[2],
            'units': cells[3],
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        array.append(cleaned_data_row)

    return array

get_newest_bananas(datetime(2022, 12, 9))
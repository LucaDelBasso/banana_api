import requests, re
import json
from pyexcel_ods3 import read_data
from datetime import datetime
from bs4 import BeautifulSoup

base_url = 'https://www.gov.uk'
gov_url = f'{base_url}/government/statistical-data-sets/banana-prices'

def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    r.close()
    return soup

def get_all_bananas():
    response = requests.get(gov_url)
    csv_url = re.search(r'https:\/\/.+\/bananas-.+csv', response.text)[0]
    csv_response = requests.get(csv_url)
    return csv_response

def get_newest_bananas(last_date_in_db):
    soup = get_soup(gov_url)
    relative_url = soup.find('a', {'class': 'govuk-link', 'href': re.compile('/preview')})['href']
    
    preview_url = f'{base_url}{relative_url}'
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

def ods_to_array(response):
    file = open('current-bananas.ods', 'wb')
    file.write(response.content)
    file.close()
    data = read_data('./current-bananas.ods')
    data = data['current_week']
    updated_on = data[2][2].strftime('%Y-%m-%d')
    ROW_START = 14
    i = 0
    array = []
    while data[(ROW_START + i)][0] != '':
        country_row = data[ROW_START + i]
        row_created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        row = {
            'origin': '',
            'date': '',
            'price': '',
            'created_at': ''
            }
        array.append(row)
        i+=1
    return array
    
get_newest_bananas(datetime(2022, 12, 9))
import requests, re
import json
from pyexcel_ods3 import read_data
from datetime import datetime

gov_url = 'https://www.gov.uk/government/statistical-data-sets/banana-prices'

def get_all_bananas():
    response = requests.get(gov_url)
    csv_url = re.search(r'https:\/\/.+\/bananas-.+csv', response.text)[0]
    csv_response = requests.get(csv_url)
    return csv_response

def get_newest_bananas():
    response = requests.get(gov_url)
    ods_url = re.search(r'https:\/\/.+\/bananas-.+ods', response.text)[0]
    ods_response = requests.get(ods_url)
    print(ods_response.text)
    return ods_response

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
    

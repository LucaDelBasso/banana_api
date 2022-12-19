import requests, re

gov_url = 'https://www.gov.uk/government/statistical-data-sets/banana-prices'

def get_all_bananas():
    response = requests.get(gov_url)
    csv_url = re.search(r'https:\/\/.+\/bananas-.+csv', response.text)[0]
    csv_text = requests.get(csv_url).text
    return csv_text

def get_newest_bananas():
    response = requests.get(gov_url)
    ods_url = re.search(r'https:\/\/.+\/bananas-.+ods', response.text)[0]
    ods_response = requests.get(ods_url)
    return ods_response

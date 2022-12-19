import requests, re

gov_url = 'https://www.gov.uk/government/statistical-data-sets/banana-prices'

def get_all_data():
    response = requests.get(gov_url)
    csv_url = re.search(r'https:\/\/.+\/bananas-.+csv', response.text)[0]
    print(csv_url)
    csv_text = requests.get(csv_url).text
    return csv_text



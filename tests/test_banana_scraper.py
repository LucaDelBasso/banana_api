from libs import banana_scraper
from datetime import datetime

def test_get_data_url():
    all = banana_scraper.get_url(span_class='preview')
    assert all[0] == '/'
    latest = banana_scraper.get_url(span_class='download')
    assert latest[:5] == 'https'

def test_get_all_bananas():
    response = banana_scraper.get_all_bananas()
    assert response.status_code == 200
    assert '£' in response.text

def test_get_newest_bananas():
    mongo_last_updated = datetime(2022, 12, 9) #yyyy/mm/dd
    scraped_data = banana_scraper.get_newest_bananas(mongo_last_updated)
    
    assert type(scraped_data) is list
    try:
        assert type(scraped_data.pop()) is dict
    except: IndexError()


# def test_ods_to_array():
#     ods_response = banana_scraper.get_newest_bananas()
#     cleaned_data = banana_scraper.ods_to_array(ods_response)
#     assert type(cleaned_data) is list
#     try:
#         assert type(cleaned_data.pop()) is dict
#     except: IndexError()

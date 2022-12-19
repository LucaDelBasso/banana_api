from libs import banana_scraper

def test_get_all_bananas():
    response = banana_scraper.get_all_bananas()
    assert response.status_code == 200
    assert '£' in response.text

def test_get_newest_bananas():
    response = banana_scraper.get_newest_bananas()
    headers = response.headers
    assert response.status_code == 200
    assert 'bananas-current' in headers["Content-Disposition"]

def test_ods_to_array():
    ods_response = banana_scraper.get_newest_bananas()
    cleaned_data = banana_scraper.test_ods_to_array(ods_response)
    assert type(cleaned_data) is list
    try:
        assert type(cleaned_data.pop()) is dict
    except: IndexError()

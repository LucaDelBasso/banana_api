from libs import banana_scraper

def test_get_all_bananas():
    assert '£' in banana_scraper.get_all_bananas()

def test_get_newest_bananas():
    response = banana_scraper.get_newest_bananas()
    headers = response.headers
    assert response.status_code == 200
    assert 'bananas-current' in headers["Content-Disposition"]
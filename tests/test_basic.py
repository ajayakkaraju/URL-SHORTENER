
import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_and_redirect(client):
    # Shorten a valid URL
    resp = client.post('/api/shorten', json={'url': 'https://example.com'})
    assert resp.status_code == 201
    data = resp.get_json()
    assert 'short_code' in data
    assert 'short_url' in data
    short_code = data['short_code']

    # Redirect works
    resp2 = client.get(f'/{short_code}', follow_redirects=False)
    assert resp2.status_code == 302
    assert resp2.headers['Location'] == 'https://example.com'

def test_invalid_url(client):
    resp = client.post('/api/shorten', json={'url': 'not_a_url'})
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data

def test_missing_url(client):
    resp = client.post('/api/shorten', json={})
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data

def test_analytics_and_click_count(client):
    # Shorten a URL
    resp = client.post('/api/shorten', json={'url': 'https://pytest.org'})
    assert resp.status_code == 201
    short_code = resp.get_json()['short_code']

    # Click it 3 times
    for _ in range(3):
        client.get(f'/{short_code}')

    # Get stats
    stats = client.get(f'/api/stats/{short_code}')
    assert stats.status_code == 200
    data = stats.get_json()
    assert data['url'] == 'https://pytest.org'
    assert data['clicks'] == 3
    assert 'created_at' in data

def test_redirect_404(client):
    resp = client.get('/nope404', follow_redirects=False)
    assert resp.status_code == 404

def test_stats_404(client):
    resp = client.get('/api/stats/doesnotexist')
    assert resp.status_code == 404
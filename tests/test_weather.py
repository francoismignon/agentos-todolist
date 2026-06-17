import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_index_returns_200(client):
    """La route / doit retourner 200"""
    assert client.get("/").status_code == 200

def test_index_contains_h1_meteo(client):
    """Le HTML doit contenir un h1 avec Dashboard Météo"""
    html = client.get("/").data.decode()
    assert "<h1>Dashboard Météo</h1>" in html

def test_index_contains_city_input(client):
    """Le HTML doit contenir un input avec id city-input"""
    html = client.get("/").data.decode()
    assert 'id="city-input"' in html

def test_index_contains_search_button(client):
    """Le HTML doit contenir un bouton avec id search-btn"""
    html = client.get("/").data.decode()
    assert 'id="search-btn"' in html

def test_index_contains_weather_result_div(client):
    """Le HTML doit contenir une div avec id weather-result"""
    html = client.get("/").data.decode()
    assert 'id="weather-result"' in html

def test_index_contains_placeholder(client):
    """L'input doit avoir le placeholder Entrez une ville"""
    html = client.get("/").data.decode()
    assert 'placeholder="Entrez une ville"' in html

def test_index_contains_submit_button(client):
    """Le bouton doit être de type submit"""
    html = client.get("/").data.decode()
    assert 'type="submit"' in html

def test_index_contains_form(client):
    """Le HTML doit contenir un formulaire"""
    html = client.get("/").data.decode()
    assert "<form" in html

def test_index_contains_search_button_text(client):
    """Le bouton doit contenir le texte Rechercher"""
    html = client.get("/").data.decode()
    assert "Rechercher" in html

def test_index_contains_empty_weather_result(client):
    """La div weather-result doit être vide"""
    html = client.get("/").data.decode()
    assert '<div id="weather-result"></div>' in html
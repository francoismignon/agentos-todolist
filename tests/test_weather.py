import pytest
import json
from app import app

@pytest.fixture
def client():
    with app.test_client() as c:
        yield c

def test_index_returns_200(client):
    """La page d'accueil doit répondre 200"""
    assert client.get("/").status_code == 200

def test_index_contains_weather_form(client):
    """Le formulaire météo doit être présent"""
    html = client.get("/").data.decode()
    assert 'id="weatherForm"' in html
    assert 'id="city-input"' in html
    assert 'id="search-btn"' in html

def test_index_contains_weather_result_div(client):
    """La div de résultat météo doit exister"""
    html = client.get("/").data.decode()
    assert 'id="weather-result"' in html

def test_index_has_dark_background(client):
    """Le fond doit être sombre (1a1a2e)"""
    html = client.get("/").data.decode()
    assert '#1a1a2e' in html or 'background: linear-gradient(135deg, #1a1a2e' in html

def test_index_has_weather_js(client):
    """Le JavaScript de gestion météo doit être présent"""
    html = client.get("/").data.decode()
    assert "weatherForm" in html
    assert "fetch('/api/weather'" in html or 'fetch("/api/weather"' in html

def test_empty_city_returns_400(client):
    """POST /api/weather avec ville vide doit retourner 400"""
    response = client.post("/api/weather", json={"city": ""})
    assert response.status_code == 400

def test_empty_city_error_message(client):
    """POST /api/weather avec ville vide doit retourner un message d'erreur"""
    response = client.post("/api/weather", json={"city": ""})
    data = json.loads(response.data)
    assert "error" in data

def test_missing_city_returns_400(client):
    """POST /api/weather sans champ city doit retourner 400"""
    response = client.post("/api/weather", json={})
    assert response.status_code == 400

def test_weather_result_has_temperature_style(client):
    """Le CSS doit prévoir un affichage en gros pour la température"""
    html = client.get("/").data.decode()
    assert "font-size: 20px" in html or "font-weight: bold" in html

def test_weather_result_has_weather_info_grid(client):
    """Le CSS doit contenir la grille d'affichage météo"""
    html = client.get("/").data.decode()
    assert "weather-info" in html
    assert "grid-template-columns: 1fr 1fr" in html
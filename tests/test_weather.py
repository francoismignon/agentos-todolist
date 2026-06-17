import pytest
import json
from app import app

@pytest.fixture
def client():
    with app.test_client() as c:
        yield c

def test_health_returns_200_and_status(client):
    """GET /api/health doit retourner 200 avec status ok et version 1.0"""
    response = client.get("/api/health")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["version"] == "1.0"

def test_health_returns_json_content_type(client):
    """GET /api/health doit retourner du JSON"""
    response = client.get("/api/health")
    assert response.content_type == "application/json"

def test_index_contains_footer(client):
    """La page d'accueil doit contenir le footer avec Powered by Open-Meteo API"""
    html = client.get("/").data.decode()
    assert "Powered by Open-Meteo API" in html

def test_index_contains_weather_result_div(client):
    """La page d'accueil doit contenir #weather-result"""
    html = client.get("/").data.decode()
    assert 'id="weather-result"' in html

def test_empty_input_shows_warning(client):
    """POST /api/weather avec city vide doit retourner 400"""
    response = client.post("/api/weather", json={"city": ""})
    assert response.status_code == 400

def test_empty_input_error_message(client):
    """POST /api/weather avec city vide doit retourner un message d'erreur"""
    response = client.post("/api/weather", json={"city": ""})
    data = json.loads(response.data)
    assert "error" in data

def test_missing_city_returns_400(client):
    """POST /api/weather sans champ city doit retourner 400"""
    response = client.post("/api/weather", json={})
    assert response.status_code == 400

def test_missing_city_error_message(client):
    """POST /api/weather sans champ city doit retourner un message d'erreur"""
    response = client.post("/api/weather", json={})
    data = json.loads(response.data)
    assert "error" in data

def test_unknown_city_returns_400(client):
    """POST /api/weather avec une ville inexistante doit retourner 400"""
    response = client.post("/api/weather", json={"city": "xyzinexistant"})
    assert response.status_code == 400

def test_unknown_city_error_message(client):
    """POST /api/weather avec une ville inexistante doit retourner un message d'erreur"""
    response = client.post("/api/weather", json={"city": "xyzinexistant"})
    data = json.loads(response.data)
    assert "error" in data
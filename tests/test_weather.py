import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_weather_paris_returns_200(client):
    """POST /api/weather avec Paris doit retourner 200"""
    response = client.post("/api/weather", json={"city": "Paris"})
    assert response.status_code == 200

def test_weather_paris_contains_temperature(client):
    """POST /api/weather avec Paris doit retourner une température"""
    response = client.post("/api/weather", json={"city": "Paris"})
    data = json.loads(response.data)
    assert "temperature" in data

def test_weather_paris_contains_wind_speed(client):
    """POST /api/weather avec Paris doit retourner la vitesse du vent"""
    response = client.post("/api/weather", json={"city": "Paris"})
    data = json.loads(response.data)
    assert "wind_speed" in data

def test_weather_paris_contains_weather_code(client):
    """POST /api/weather avec Paris doit retourner le code météo"""
    response = client.post("/api/weather", json={"city": "Paris"})
    data = json.loads(response.data)
    assert "weather_code" in data

def test_weather_paris_contains_city(client):
    """POST /api/weather avec Paris doit retourner le nom de la ville"""
    response = client.post("/api/weather", json={"city": "Paris"})
    data = json.loads(response.data)
    assert data["city"] == "Paris"

def test_weather_unknown_city_returns_400(client):
    """POST /api/weather avec une ville inexistante doit retourner 400"""
    response = client.post("/api/weather", json={"city": "xyzinexistant"})
    assert response.status_code == 400

def test_weather_unknown_city_returns_error_message(client):
    """POST /api/weather avec une ville inexistante doit retourner un message d'erreur"""
    response = client.post("/api/weather", json={"city": "xyzinexistant"})
    data = json.loads(response.data)
    assert "error" in data

def test_weather_missing_city_returns_400(client):
    """POST /api/weather sans champ city doit retourner 400"""
    response = client.post("/api/weather", json={})
    assert response.status_code == 400

def test_weather_empty_city_returns_400(client):
    """POST /api/weather avec city vide doit retourner 400"""
    response = client.post("/api/weather", json={"city": ""})
    assert response.status_code == 400

def test_weather_temperature_is_number(client):
    """POST /api/weather avec Paris doit retourner une température numérique"""
    response = client.post("/api/weather", json={"city": "Paris"})
    data = json.loads(response.data)
    assert isinstance(data["temperature"], (int, float))
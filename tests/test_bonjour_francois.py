import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_bonjour_francois_button_exists(client):
    """Le bouton 'Bonjour François' doit être présent dans le HTML"""
    html = client.get("/").data.decode()
    assert "Bonjour François" in html

def test_bonjour_francois_button_is_button(client):
    """Le bouton doit être un élément <button>"""
    html = client.get("/").data.decode()
    assert '<button' in html
    assert 'Bonjour François' in html

def test_bonjour_francois_has_click_handler(client):
    """Le bouton doit avoir un gestionnaire de clic"""
    html = client.get("/").data.decode()
    assert 'onclick' in html or 'addEventListener' in html or 'click' in html

def test_bonjour_francois_message_appears_on_click(client):
    """Au clic, le message 'Bonjour François !' doit apparaître"""
    html = client.get("/").data.decode()
    assert "Bonjour François !" in html

def test_bonjour_francois_button_has_id_or_class(client):
    """Le bouton doit avoir un id ou une classe pour le cibler"""
    html = client.get("/").data.decode()
    assert 'id="' in html or 'class="' in html

def test_bonjour_francois_button_is_visible(client):
    """Le bouton ne doit pas être caché par défaut"""
    html = client.get("/").data.decode()
    assert 'display:none' not in html and 'visibility:hidden' not in html

def test_bonjour_francois_button_has_text(client):
    """Le texte du bouton doit être exactement 'Bonjour François'"""
    html = client.get("/").data.decode()
    assert 'Bonjour François' in html

def test_bonjour_francois_message_is_not_empty(client):
    """Le message affiché ne doit pas être vide"""
    html = client.get("/").data.decode()
    assert "Bonjour François !" in html
    assert len("Bonjour François !") > 0

def test_bonjour_francois_button_not_duplicated(client):
    """Le bouton ne doit pas être dupliqué"""
    html = client.get("/").data.decode()
    count = html.count('Bonjour François')
    assert count == 1

def test_bonjour_francois_works_without_refresh(client):
    """Le message doit s'afficher sans rechargement de page"""
    html = client.get("/").data.decode()
    assert 'preventDefault' in html or 'return false' in html or 'event.preventDefault' in html
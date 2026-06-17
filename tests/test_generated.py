# tests/test_generated.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_contains_form(client):
    """Test que la page contient un formulaire"""
    response = client.get('/')
    html = response.data.decode()
    assert '<form' in html

def test_index_contains_input_text(client):
    """Test que la page contient un input texte"""
    response = client.get('/')
    html = response.data.decode()
    assert 'type="text"' in html or 'type="input"' in html

def test_index_contains_submit_button(client):
    """Test que la page contient un bouton de soumission"""
    response = client.get('/')
    html = response.data.decode()
    assert 'type="submit"' in html or 'Ajouter' in html

def test_index_contains_form_action(client):
    """Test que le formulaire a une action POST"""
    response = client.get('/')
    html = response.data.decode()
    assert 'method="post"' in html or 'method="POST"' in html or '/api/tasks' in html

def test_index_form_has_input_name(client):
    """Test que l'input a un attribut name"""
    response = client.get('/')
    html = response.data.decode()
    assert 'name=' in html

def test_index_form_has_placeholder(client):
    """Test que l'input a un placeholder"""
    response = client.get('/')
    html = response.data.decode()
    assert 'placeholder' in html

def test_index_form_has_required(client):
    """Test que l'input a required ou une validation"""
    response = client.get('/')
    html = response.data.decode()
    assert 'required' in html or 'minlength' in html

def test_index_form_has_id(client):
    """Test que le formulaire a un id"""
    response = client.get('/')
    html = response.data.decode()
    assert 'id="' in html

def test_index_form_has_label(client):
    """Test que l'input a un label associé"""
    response = client.get('/')
    html = response.data.decode()
    assert '<label' in html

def test_index_form_has_button_text(client):
    """Test que le bouton a du texte"""
    response = client.get('/')
    html = response.data.decode()
    assert 'Ajouter' in html or 'button' in html

def test_index_form_has_event_handler(client):
    """Test que le formulaire a un gestionnaire d'événement submit"""
    response = client.get('/')
    html = response.data.decode()
    assert 'onsubmit' in html or 'addEventListener' in html

def test_index_form_has_prevent_default(client):
    """Test que le formulaire empêche le rechargement par défaut"""
    response = client.get('/')
    html = response.data.decode()
    assert 'preventDefault' in html

def test_index_form_has_fetch_or_ajax(client):
    """Test que le formulaire utilise fetch ou AJAX"""
    response = client.get('/')
    html = response.data.decode()
    assert 'fetch' in html or 'XMLHttpRequest' in html

def test_index_form_has_post_method(client):
    """Test que le formulaire utilise POST"""
    response = client.get('/')
    html = response.data.decode()
    assert 'POST' in html or 'post' in html

def test_index_form_has_api_endpoint(client):
    """Test que le formulaire appelle /api/tasks"""
    response = client.get('/')
    html = response.data.decode()
    assert '/api/tasks' in html
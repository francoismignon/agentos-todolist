# tests/test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_status(client):
    """Test que la page d'accueil retourne un statut 200"""
    response = client.get('/')
    assert response.status_code == 200

def test_index_content_type(client):
    """Test que la réponse est du HTML"""
    response = client.get('/')
    assert response.content_type == 'text/html; charset=utf-8'

def test_index_contains_checkbox(client):
    """Test que la page contient un input checkbox"""
    response = client.get('/')
    assert 'type="checkbox"' in response.data.decode()

def test_index_contains_app_div(client):
    """Test que la page contient le div #app"""
    response = client.get('/')
    assert '<div id="app">' in response.data.decode()

def test_index_contains_strike_script(client):
    """Test que la page contient du JavaScript pour barrer le texte"""
    response = client.get('/')
    html = response.data.decode()
    assert 'text-decoration' in html or 'line-through' in html

def test_index_contains_event_listener(client):
    """Test que la page contient un écouteur d'événement change"""
    response = client.get('/')
    html = response.data.decode()
    assert 'addEventListener' in html or 'onchange' in html or 'onclick' in html

def test_index_contains_task_elements(client):
    """Test que la page contient des éléments de tâche"""
    response = client.get('/')
    html = response.data.decode()
    assert 'li' in html or 'task' in html.lower() or 'todo' in html.lower()

def test_index_has_correct_structure(client):
    """Test que la structure HTML de base est présente"""
    response = client.get('/')
    html = response.data.decode()
    assert '<!DOCTYPE html>' in html
    assert '<html>' in html
    assert '<head>' in html
    assert '<body>' in html

def test_index_links_stylesheet(client):
    """Test que la page lie le fichier CSS"""
    response = client.get('/')
    assert 'style.css' in response.data.decode()

def test_index_has_title(client):
    """Test que la page a un titre"""
    response = client.get('/')
    assert '<title>' in response.data.decode()

def test_index_no_errors(client):
    """Test qu'aucune erreur serveur n'est retournée"""
    response = client.get('/')
    assert response.status_code < 500

def test_index_not_empty(client):
    """Test que la réponse n'est pas vide"""
    response = client.get('/')
    assert len(response.data) > 0

def test_index_contains_script_tag(client):
    """Test que la page contient une balise script"""
    response = client.get('/')
    assert '<script>' in response.data.decode()

def test_index_checkbox_has_id_or_class(client):
    """Test que les checkboxes ont un attribut pour les cibler"""
    response = client.get('/')
    html = response.data.decode()
    # Vérifie que les checkboxes ont un id ou une classe
    assert 'id=' in html or 'class=' in html

def test_index_multiple_checkboxes(client):
    """Test qu'il y a plusieurs checkboxes (pour plusieurs tâches)"""
    response = client.get('/')
    html = response.data.decode()
    count = html.count('type="checkbox"')
    assert count >= 2  # Au moins 2 tâches avec checkbox
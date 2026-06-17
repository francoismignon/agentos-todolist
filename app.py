from flask import Flask, render_template_string, request, jsonify
import requests
import json

app = Flask(__name__)

# Configuration
API_BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Stockage simple des tâches en mémoire
tasks = []
task_id_counter = 0

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Météo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        #app {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            padding: 30px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        h1 {
            color: #1a1a2e;
            text-align: center;
            margin-bottom: 20px;
        }
        .add-form {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        .add-form input {
            flex: 1;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.3s;
        }
        .add-form input:focus {
            border-color: #0f3460;
        }
        .add-form button {
            padding: 12px 24px;
            background: #0f3460;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }
        .add-form button:hover {
            background: #1a1a2e;
        }
        #weather-result {
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 8px;
            display: none;
        }
        #weather-result.show {
            display: block;
        }
        #weather-result.error {
            background: #ffe6e6;
            color: #cc0000;
            border: 1px solid #ffcccc;
        }
        #weather-result.success {
            background: #e6f3ff;
            border: 1px solid #b3d9ff;
        }
        .weather-info {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        .weather-info .label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .weather-info .value {
            font-size: 18px;
            font-weight: bold;
            color: #1a1a2e;
        }
        .weather-card {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
        }
        .weather-card .city-name {
            font-size: 24px;
            font-weight: bold;
            color: #1a1a2e;
            margin-bottom: 15px;
        }
        .weather-card .temperature {
            font-size: 48px;
            font-weight: bold;
            color: #0f3460;
            text-align: center;
            margin-bottom: 15px;
        }
        .weather-card .details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        .weather-card .detail-item {
            text-align: center;
            padding: 10px;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 8px;
        }
        .weather-card .detail-item .label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .weather-card .detail-item .value {
            font-size: 18px;
            font-weight: bold;
            color: #1a1a2e;
        }
        .loader {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .loader.show {
            display: block;
        }
        .loader::after {
            content: '';
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #0f3460;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        #taskList {
            margin-top: 20px;
        }
        .task-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            border-bottom: 1px solid #e0e0e0;
        }
        .task-item input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }
        .task-item label {
            font-size: 16px;
            color: #333;
            cursor: pointer;
        }
        .task-item input[type="checkbox"]:checked + label {
            text-decoration: line-through;
            color: #999;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            color: #666;
            font-size: 12px;
        }
        .bonjour-btn {
            display: block;
            width: 100%;
            padding: 12px 24px;
            background: #e94560;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: background 0.3s, transform 0.2s;
            margin-bottom: 20px;
        }
        .bonjour-btn:hover {
            background: #d63851;
            transform: translateY(-2px);
        }
        .bonjour-btn:active {
            transform: translateY(0);
        }
        .bonjour-message {
            text-align: center;
            padding: 15px;
            margin-bottom: 20px;
            background: #e6f3ff;
            border: 1px solid #b3d9ff;
            border-radius: 8px;
            color: #0f3460;
            font-size: 18px;
            font-weight: bold;
            display: none;
        }
        .bonjour-message.show {
            display: block;
        }
    </style>
</head>
<body>
    <div id="app">
        <h1>Dashboard Météo</h1>
        <button class="bonjour-btn" id="bonjourBtn">Bonjour François</button>
        <div class="bonjour-message" id="bonjourMessage">Bonjour François !</div>
        <form class="add-form" id="weatherForm">
            <input type="text" id="city-input" placeholder="Entrez une ville">
            <button type="submit" id="search-btn">Rechercher</button>
        </form>
        <div class="loader" id="loader"></div>
        <div id="weather-result"></div>
        <form class="add-form" id="addForm">
            <input type="text" id="taskInput" placeholder="Nouvelle tâche...">
            <button type="submit">Ajouter</button>
        </form>
        <div id="taskList">
            {% for task in tasks %}
            <div class="task-item">
                <input type="checkbox" id="task{{ task.id }}" {% if task.done %}checked{% endif %}>
                <label for="task{{ task.id }}">{{ task.text }}</label>
            </div>
            {% endfor %}
        </div>
        <div class="footer">Powered by Open-Meteo API</div>
    </div>
    <script>
        document.getElementById('bonjourBtn').addEventListener('click', function() {
            const message = document.getElementById('bonjourMessage');
            message.classList.toggle('show');
        });

        document.getElementById('weatherForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const city = document.getElementById('city-input').value.trim();
            const resultDiv = document.getElementById('weather-result');
            const loader = document.getElementById('loader');
            
            if (!city) {
                resultDiv.innerHTML = '<div class="error">Veuillez entrer une ville</div>';
                resultDiv.className = 'show error';
                return;
            }
            
            loader.classList.add('show');
            resultDiv.className = '';
            resultDiv.innerHTML = '';
            
            try {
                const response = await fetch('/api/weather', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({city: city})
                });
                
                const data = await response.json();
                loader.classList.remove('show');
                
                if (response.ok) {
                    resultDiv.innerHTML = `
                        <div class="weather-card">
                            <div class="city-name">${data.city}</div>
                            <div class="temperature">${data.temperature}°C</div>
                            <div class="details">
                                <div class="detail-item">
                                    <div class="label">Ressenti</div>
                                    <div class="value">${data.feels_like}°C</div>
                                </div>
                                <div class="detail-item">
                                    <div class="label">Humidité</div>
                                    <div class="value">${data.humidity}%</div>
                                </div>
                                <div class="detail-item">
                                    <div class="label">Vent</div>
                                    <div class="value">${data.wind_speed} km/h</div>
                                </div>
                                <div class="detail-item">
                                    <div class="label">Précipitations</div>
                                    <div class="value">${data.precipitation} mm</div>
                                </div>
                            </div>
                        </div>
                    `;
                    resultDiv.className = 'show success';
                } else {
                    resultDiv.innerHTML = `<div class="error">${data.error || 'Erreur lors de la récupération des données'}</div>`;
                    resultDiv.className = 'show error';
                }
            } catch (error) {
                loader.classList.remove('show');
                resultDiv.innerHTML = '<div class="error">Erreur de connexion au serveur</div>';
                resultDiv.className = 'show error';
            }
        });

        document.getElementById('addForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const input = document.getElementById('taskInput');
            const text = input.value.trim();
            
            if (!text) return;
            
            try {
                const response = await fetch('/api/tasks', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({text: text})
                });
                
                if (response.ok) {
                    input.value = '';
                    location.reload();
                }
            } catch (error) {
                console.error('Erreur:', error);
            }
        });

        document.querySelectorAll('#taskList input[type="checkbox"]').forEach(checkbox => {
            checkbox.addEventListener('change', async function() {
                const taskId = this.id.replace('task', '');
                try {
                    await fetch('/api/tasks/' + taskId, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({done: this.checked})
                    });
                } catch (error) {
                    console.error('Erreur:', error);
                }
            });
        });
    </script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route('/api/weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    
    if not data or 'city' not in data:
        return jsonify({'error': 'Ville non spécifiée'}), 400
    
    city = data['city'].strip()
    
    if not city:
        return jsonify({'error': 'Ville non spécifiée'}), 400
    
    try:
        # Géocodage de la ville
        geo_response = requests.get(GEOCODING_URL, params={
            'name': city,
            'count': 1,
            'language': 'fr',
            'format': 'json'
        })
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data.get('results'):
            return jsonify({'error': f'Ville "{city}" non trouvée'}), 404
        
        location = geo_data['results'][0]
        lat = location['latitude']
        lon = location['longitude']
        city_name = location.get('name', city)
        country = location.get('country', '')
        
        # Récupération des données météo
        weather_response = requests.get(API_BASE_URL, params={
            'latitude': lat,
            'longitude': lon,
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m',
            'timezone': 'auto'
        })
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        current = weather_data['current']
        
        return jsonify({
            'city': f"{city_name}, {country}" if country else city_name,
            'temperature': round(current['temperature_2m']),
            'feels_like': round(current['apparent_temperature']),
            'humidity': current['relative_humidity_2m'],
            'wind_speed': round(current['wind_speed_10m']),
            'precipitation': current['precipitation']
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Erreur de connexion au service météo'}), 500

@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    global task_id_counter
    
    if request.method == 'GET':
        return jsonify(tasks)
    
    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Texte de la tâche requis'}), 400
        
        task_id_counter += 1
        task = {
            'id': task_id_counter,
            'text': data['text'],
            'done': False
        }
        tasks.append(task)
        return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    
    for task in tasks:
        if task['id'] == task_id:
            if 'done' in data:
                task['done'] = data['done']
            if 'text' in data:
                task['text'] = data['text']
            return jsonify(task)
    
    return jsonify({'error': 'Tâche non trouvée'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
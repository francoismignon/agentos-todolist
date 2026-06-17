from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

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
        }
        .weather-info .value {
            font-size: 20px;
            font-weight: bold;
            color: #1a1a2e;
        }
        .task-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
        .task-item:last-child {
            border-bottom: none;
        }
        .task-item input[type="checkbox"] {
            width: 18px;
            height: 18px;
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
            margin-top: 20px;
            text-align: center;
            color: #999;
            font-size: 12px;
        }
        .loader {
            display: none;
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #0f3460;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        .loader.show {
            display: block;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .weather-card {
            background: rgba(15, 52, 96, 0.1);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }
        .weather-card .city-name {
            font-size: 24px;
            font-weight: bold;
            color: #1a1a2e;
            margin-bottom: 15px;
            text-align: center;
        }
        .weather-card .temperature {
            font-size: 3em;
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
    </style>
</head>
<body>
    <div id="app">
        <h1>Dashboard Météo</h1>
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
        document.getElementById('weatherForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const city = document.getElementById('city-input').value.trim();
            const resultDiv = document.getElementById('weather-result');
            const loader = document.getElementById('loader');
            
            if (!city) {
                resultDiv.innerHTML = 'Entrez un nom de ville';
                resultDiv.className = 'error show';
                return;
            }
            
            loader.classList.add('show');
            resultDiv.className = '';
            resultDiv.innerHTML = '';
            
            try {
                const response = await fetch('/api/weather', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({city: city})
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    loader.classList.remove('show');
                    resultDiv.innerHTML = error.error || 'Ville non trouvée';
                    resultDiv.className = 'error show';
                    return;
                }
                
                const data = await response.json();
                const weatherCodeDescriptions = {
                    0: 'Ciel dégagé',
                    1: 'Principalement dégagé',
                    2: 'Partiellement nuageux',
                    3: 'Nuageux',
                    45: 'Brouillard',
                    48: 'Brouillard givrant',
                    51: 'Bruine légère',
                    53: 'Bruine modérée',
                    55: 'Bruine dense',
                    56: 'Bruine verglaçante légère',
                    57: 'Bruine verglaçante dense',
                    61: 'Pluie légère',
                    63: 'Pluie modérée',
                    65: 'Pluie forte',
                    66: 'Pluie verglaçante légère',
                    67: 'Pluie verglaçante forte',
                    71: 'Neige légère',
                    73: 'Neige modérée',
                    75: 'Neige forte',
                    77: 'Grains de neige',
                    80: 'Averses de pluie légères',
                    81: 'Averses de pluie modérées',
                    82: 'Averses de pluie violentes',
                    85: 'Averses de neige légères',
                    86: 'Averses de neige fortes',
                    95: 'Orage',
                    96: 'Orage avec grêle légère',
                    99: 'Orage avec grêle forte'
                };
                const description = weatherCodeDescriptions[data.weathercode] || 'Non disponible';
                
                loader.classList.remove('show');
                resultDiv.innerHTML = `
                    <div class="weather-card">
                        <div class="city-name">${data.city}</div>
                        <div class="temperature">${data.temperature}°C</div>
                        <div class="details">
                            <div class="detail-item">
                                <div class="label">Vent</div>
                                <div class="value">${data.wind} km/h</div>
                            </div>
                            <div class="detail-item">
                                <div class="label">Description</div>
                                <div class="value">${description}</div>
                            </div>
                        </div>
                    </div>
                `;
                resultDiv.className = 'success show';
            } catch (error) {
                loader.classList.remove('show');
                resultDiv.innerHTML = 'Erreur de connexion au serveur';
                resultDiv.className = 'error show';
            }
        });
    </script>
</body>
</html>"""

tasks = []
task_id_counter = 0

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route("/api/weather", methods=["POST"])
def get_weather():
    data = request.get_json()
    city = data.get("city", "").strip()
    
    if not city:
        return jsonify({"error": "Le champ city est requis"}), 400
    
    # Geocoding
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_response = requests.get(geo_url)
    
    if geo_response.status_code != 200:
        return jsonify({"error": "Erreur lors de la recherche de la ville"}), 500
    
    geo_data = geo_response.json()
    
    if not geo_data.get("results"):
        return jsonify({"error": f"Ville '{city}' non trouvée"}), 400
    
    location = geo_data["results"][0]
    lat = location["latitude"]
    lon = location["longitude"]
    city_name = location.get("name", city)
    
    # Météo
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_response = requests.get(weather_url)
    
    if weather_response.status_code != 200:
        return jsonify({"error": "Erreur lors de la récupération des données météo"}), 500
    
    weather_data = weather_response.json()
    current = weather_data.get("current_weather", {})
    
    return jsonify({
        "city": city_name,
        "temperature": current.get("temperature"),
        "wind": current.get("windspeed"),
        "weathercode": current.get("weathercode")
    })

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
def add_task():
    global task_id_counter
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Le champ text est requis"}), 400
    task_id_counter += 1
    task = {"id": task_id_counter, "text": text, "done": False}
    tasks.append(task)
    return jsonify(task), 201

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id:
            if "text" in data:
                task["text"] = data["text"]
            if "done" in data:
                task["done"] = data["done"]
            return jsonify(task)
    return jsonify({"error": "Tâche non trouvée"}), 404

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Tâche supprimée"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
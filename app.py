from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

tasks = [
    {"id": 1, "text": "Faire les courses", "done": False},
    {"id": 2, "text": "Appeler le médecin", "done": False},
    {"id": 3, "text": "Réviser le code", "done": False}
]

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
            margin-bottom: 25px;
            font-size: 28px;
        }
        .add-form {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        .add-form input[type="text"] {
            flex: 1;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 6px;
        }
        .add-form button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #1a1a2e;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        .add-form button:hover {
            background-color: #2d2d5e;
        }
        #weather-result {
            margin-bottom: 20px;
            padding: 15px;
            background: #f0f4ff;
            border-radius: 8px;
            display: none;
        }
        #weather-result.show {
            display: block;
        }
        #weather-result.error {
            background: #ffe0e0;
            color: #c00;
        }
        .weather-info {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        .weather-info div {
            padding: 10px;
            background: white;
            border-radius: 6px;
            text-align: center;
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
    </style>
</head>
<body>
    <div id="app">
        <h1>Dashboard Météo</h1>
        <form class="add-form" id="weatherForm">
            <input type="text" id="city-input" placeholder="Entrez une ville">
            <button type="submit" id="search-btn">Rechercher</button>
        </form>
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
    </div>
    <script>
        document.getElementById('weatherForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const city = document.getElementById('city-input').value.trim();
            const resultDiv = document.getElementById('weather-result');
            
            if (!city) {
                resultDiv.innerHTML = 'Veuillez entrer une ville';
                resultDiv.className = 'error show';
                return;
            }
            
            try {
                const response = await fetch('/api/weather', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({city: city})
                });
                
                if (!response.ok) {
                    const error = await response.json();
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
                    61: 'Pluie légère',
                    63: 'Pluie modérée',
                    65: 'Pluie forte',
                    71: 'Neige légère',
                    73: 'Neige modérée',
                    75: 'Neige forte',
                    80: 'Averses de pluie légères',
                    81: 'Averses de pluie modérées',
                    82: 'Averses de pluie violentes',
                    95: 'Orage',
                    96: 'Orage avec grêle légère',
                    99: 'Orage avec grêle forte'
                };
                const description = weatherCodeDescriptions[data.weathercode] || 'Inconnu';
                
                resultDiv.innerHTML = `
                    <h3 style="margin-bottom:15px;color:#1a1a2e;">Météo à ${data.city}</h3>
                    <div class="weather-info">
                        <div>
                            <div class="label">Température</div>
                            <div class="value">${data.temperature}°C</div>
                        </div>
                        <div>
                            <div class="label">Vent</div>
                            <div class="value">${data.wind} km/h</div>
                        </div>
                        <div style="grid-column:1/3;">
                            <div class="label">Description</div>
                            <div class="value">${description}</div>
                        </div>
                    </div>
                `;
                resultDiv.className = 'show';
            } catch (error) {
                resultDiv.innerHTML = 'Erreur de connexion au serveur';
                resultDiv.className = 'error show';
            }
        });
        
        document.getElementById('addForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const input = document.getElementById('taskInput');
            const text = input.value.trim();
            if (!text) return;
            
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})
            });
            
            if (response.ok) {
                const task = await response.json();
                const taskList = document.getElementById('taskList');
                const div = document.createElement('div');
                div.className = 'task-item';
                div.innerHTML = `
                    <input type="checkbox" id="task${task.id}">
                    <label for="task${task.id}">${task.text}</label>
                `;
                taskList.appendChild(div);
                input.value = '';
            }
        });
    </script>
</body>
</html>"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Le champ ne peut pas être vide"}), 400
    new_id = max(task["id"] for task in tasks) + 1 if tasks else 1
    tasks.append({"id": new_id, "text": text, "done": False})
    return jsonify({"id": new_id, "text": text, "done": False}), 201

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
        return jsonify({"error": "Erreur lors de la récupération de la météo"}), 500
    
    weather_data = weather_response.json()
    current = weather_data.get("current_weather", {})
    
    return jsonify({
        "city": city_name,
        "temperature": current.get("temperature"),
        "wind": current.get("windspeed"),
        "weathercode": current.get("weathercode")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
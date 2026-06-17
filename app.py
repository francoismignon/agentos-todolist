from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

tasks = [
    {"id": 1, "text": "Faire les courses", "done": False},
    {"id": 2, "text": "Appeler le médecin", "done": False},
    {"id": 3, "text": "Réviser le code", "done": False}
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Application</title>
    <link rel="stylesheet" type="text/css" href="/static/style.css">
    <style>
        .task-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 0;
        }
        .task-item input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }
        .task-item label {
            font-size: 18px;
            cursor: pointer;
            user-select: none;
        }
        .task-item input[type="checkbox"]:checked + label {
            text-decoration: line-through;
            color: #888;
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
    </style>
</head>
<body>
    <div id="app">
        <h1>Dashboard Météo</h1>
        <form class="add-form" id="addForm">
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
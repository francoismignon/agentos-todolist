from flask import Flask, render_template_string

app = Flask(__name__)

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
    </style>
</head>
<body>
    <div id="app">
        <div class="task-item">
            <input type="checkbox" id="task1">
            <label for="task1">Faire les courses</label>
        </div>
        <div class="task-item">
            <input type="checkbox" id="task2">
            <label for="task2">Appeler le médecin</label>
        </div>
        <div class="task-item">
            <input type="checkbox" id="task3">
            <label for="task3">Réviser le code</label>
        </div>
    </div>
</body>
</html>"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

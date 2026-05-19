from flask import Flask, render_template
from render import build_timeline_elements
import json

app = Flask(__name__)

def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"

@app.route('/')
def index():
    nodes = {
        "Comida": (-700, 2026, "#88CC88"),
        "Bacon": (-290, 350, "#ddcc44"),
        "Calabresa": (-350, 800, "#cc4466"),
        "Salada": (-625, -100, "#22EE32"),
        "Carne": (400, 1100, "#7E2135")
    }

    bifurcations = [
        ("Comida", "Bacon"),
        ("Comida", "Calabresa"),
        ("Comida", "Salada"),
        ("Comida", "Carne")
    ]

    y_tracks = {
        "Comida": 0, "Bacon": -60, "Calabresa": 60, "Salada": -120, "Carne": -60
    }

    philosophers = [
        ("Francis Bacon", -69, "bacon.png")
    ]

    historical_epochs = [
        {"year": -600, "label": "Período Pré-Socrático"},
        {"year": -400, "label": "Grécia Clássica"},
        {"year": 0,    "label": "Início da Era Comum"},
        {"year": 500,  "label": "Alta Idade Média"},
        {"year": 1200, "label": "Baixa Idade Média"},
        {"year": 1500, "label": "Renascimento / Idade Moderna"},
        {"year": 1800, "label": "Séc XIX / Contemp."},
        {"year": 2000, "label": "Séc XXI"}
    ]

    elements, total_width, min_year, scale_x = build_timeline_elements(nodes, bifurcations, y_tracks)

    for epoch in historical_epochs:
        epoch['x'] = (epoch['year'] - min_year) * scale_x

    return render_template(
        'index.html', 
        elements_json=json.dumps(elements),
        epochs=historical_epochs,
        total_width=total_width
    )

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
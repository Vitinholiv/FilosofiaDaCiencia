from flask import Flask, render_template
from render import build_timeline_elements, hex_to_rgba
import json

app = Flask(__name__)

@app.route('/')
def index():
    nodes = {
        "Comida": (-600, -300, "#88CC88"),
        "Bacon": (-290, 600, "#ddcc44"),
        "Calabresa": (-280, 610, "#cc4466")
    }

    bifurcations = [
        ("Comida", "Bacon"),
        ("Comida", "Calabresa")
    ]

    y_tracks = {
        "Comida": 0, "Bacon": -120, "Calabresa": 120
    }

    philosophers = [
        ("Francis Bacon", -69, "bacon.png")
    ]

    """ 
    Visualização de trabalhos publicados no canto inferior da tela.
    Inspirado em https://pt.mathigon.org/timeline
    """
    # Formato: (ano, texto do balão, cor)
    bottom_events = [
        (-400, "-400: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#cc0066"),
        (-300, "-300: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#008800"),
        (-200, "-200: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#cc0000")
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

    # Agora build_timeline_elements também recebe bottom_events como argumento
    elements, total_width, min_year, scale_x = build_timeline_elements(nodes, bifurcations, y_tracks, bottom_events)

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
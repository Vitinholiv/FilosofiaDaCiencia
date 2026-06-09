from flask import Flask, render_template
from render import build_timeline_elements, hex_to_rgba
import json

app = Flask(__name__)

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

    """ 
    Visualização de trabalhos publicados no canto inferior da tela.
    Inspirado em https://pt.mathigon.org/timeline
    """
    # Formato: (ano, offset_y, texto do balão, cor)
    # Exemplo: Se bottom_y = 300 e offset_y = 80, o cículo terá seu centro com coordenada y bottom_y + offset_y = 380
    # Recall que y "cresce" para baixo na tela

    bottom_events = [
        (-400, 0, "-400: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#cc0066"),
        (-380, 10, "-400: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#ff9100"),
        (-360, 20, "-400: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#00ffff"),
        (-340, 30, "-400: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#6f00ff"),
        (-320, 0, "-300: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#008800"),
        (-300, 10, "-200: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#ffffff"),
        (-280, 20, "50: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#ffee07"),
        (-260, 30, "50: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#ff0883"),
        (-200, 0, "50: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#ff0000"),
        (-200, 30, "50: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#ffee00"),
        (-200, 60, "50: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#7afd00"),
        (2004, 0, "2004: Nasce o proeminente matemático Vitor Hugo de Souza.", "#60ff03"),
        (1980, 0, "1980: Morre John Lennon.", "#00f7ff")
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

    # Aqui passamos a lista philosophers como último argumento
    elements, total_width, min_year, scale_x = build_timeline_elements(nodes, bifurcations, y_tracks, bottom_events, philosophers)

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

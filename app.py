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
    
    
    # Formato: (nome, ano, offset, imagem, resumo, btn_data)
    #
    # btn_data aceita:
    #   'Contrários':  [ [nome, descricao], ... ]
    #   'Adeptos':     [ [nome, descricao], ... ]
    #   'Influenciado': {
    #       'Concorda': [ [nome, descricao], ... ],
    #       'Discorda': [ [nome, descricao], ... ]
    #   }
    #   'Obras':       [ [titulo, descricao], ... ]
 
    philosophers = [
        ("Francis Bacon", -69, 150, "static/img/bacon.png", 'Barriga de porco defumada', {
            'Contrários': [
                ('Calabresa', 'Calabresa tem muito sal!'),
                ('Salada',    'Salada é muito ruim!')
            ],
            'Adeptos': [
                ['Variedades', 'Variedades é o futuro!']
            ],
            'Influenciado': {
                'Concorda': [['Pepino', 'Pepino é bom demais!']],
                'Discorda': [['Alface', 'Alface é ruim demais!']]
            },
            'Obras': [
                ['Rubrica',    'Ano 1 - Falava sobre a Rubrica'],
                ['Kopesh',     'Ano 2 - Falava sobre um machado'],
                ['Fogueteiro', 'Ano 3 - Falava sobre um foguete']
            ],
        }),
        ("Francis Calabresa", 142, 150, "static/img/calabresa.png", 'Embutido feito com carne', {
            'Contrários':   [['Bacon', 'Bacon é gorduroso demais!']],
            'Adeptos':      [['Carne', 'Carne é nossa origem!']],
            'Influenciado': {
                'Concorda': [['Carne', 'Compartilhamos a origem animal.']],
                'Discorda': [['Salada', 'Vegetais não têm sabor.']]
            },
            'Obras': [
                ['Defumados', 'Ano 1 - Tratado sobre defumação']
            ],
        }),
        ("Francis Pepino", -500, -60, "static/img/pepino.png", 'Vegetal', {
            'Contrários':   [['Bacon', 'Carne é desnecessária!']],
            'Adeptos':      [['Alface', 'Juntos somos mais verdes!']],
            'Influenciado': {
                'Concorda': [['Alface', 'Partilhamos a leveza.']],
                'Discorda': [['Calabresa', 'Embutidos são nocivos.']]
            },
            'Obras': [
                ['Verde Vivo', 'Ano 1 - Manifesto vegetal']
            ],
        }),
        ("Francis Alface", -132, 50, "static/img/alface.png", 'Outro vegetal', {
            'Contrários':   [['Calabresa', 'Processados são o mal!']],
            'Adeptos':      [['Pepino', 'Unidos pelo verde!']],
            'Influenciado': {
                'Concorda': [['Pepino', 'Somos ambos refrescantes.']],
                'Discorda': [['Bacon', 'Gordura em excesso é ruim.']]
            },
            'Obras': [],
        }),
        ("Francis Alcatra", 290, -100, "static/img/alcatra.png", 'Bovinae', {
            'Contrários':   [['Salada', 'Salada não sustenta!']],
            'Adeptos':      [['Calabresa', 'Ambos somos proteína!']],
            'Influenciado': {
                'Concorda': [['Carne', 'Mesma família, mesmo propósito.']],
                'Discorda': [['Pepino', 'Vegetais são insuficientes.']]
            },
            'Obras': [
                ['Cortes Nobres', 'Ano 1 - Guia de cortes bovinos']
            ],
        }),
        ("Francis Variedades", -700, 0, "static/img/variedades.png", 'Cortes de vários animais', {
            'Contrários':   [],
            'Adeptos':      [['Bacon', 'Bacon abraça a variedade!']],
            'Influenciado': {
                'Concorda': [['Calabresa', 'Diversidade é riqueza.']],
                'Discorda': []
            },
            'Obras': [
                ['Pluralidade', 'Ano 1 - Sobre a diversidade animal']
            ],
        }),
    ]

    """ 
    Visualização de trabalhos publicados no canto inferior da tela.
    Inspirado em https://pt.mathigon.org/timeline
    """
    # Formato: (ano, texto do balão, cor, offset_y)
    # Exemplo: Se bottom_y = 300 e offset_y = 80, o cículo terá seu centro com coordenada y bottom_y + offset_y = 380
    # Recall que y "cresce" para baixo na tela

    bottom_events = [
        (-400, "-400: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#cc0066", 0),
        (-380, "-400: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#ff9100", 10),
        (-360, "-400: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#00ffff", 20),
        (-340, "-400: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#6f00ff", 30),
        (-320, "-300: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#008800", 0),
        (-300, "-200: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#ffffff", 10),
        (-280, "50: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#ffee07", 20),
        (-260, "50: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#ff0883", 30),
        (-200, "50: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#ff0000", 0),
        (-200, "50: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#ffee00", 30),
        (-200, "50: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", "#7afd00", 60),
        (2004, "2004: Nasce o proeminente matemático Vitor Hugo de Souza.", "#60ff03", 0)
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

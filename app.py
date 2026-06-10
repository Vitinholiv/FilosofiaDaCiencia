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

    # Formato: (ano, offset_y, lista de url de imagens, texto do balão, cor)
    # Exemplo: Se bottom_y = 300 e offset_y = 80, o cículo terá seu centro com coordenada y bottom_y + offset_y = 380
    # Recall que y "cresce" para baixo na tela

    # links são suportados em texto com sintaxe html: <a href=source_link> texto_linl </a>

    _imagem1 = "https://upload.wikimedia.org/wikipedia/commons/e/e0/Cat_demonstrating_static_cling_with_styrofoam_peanuts.jpg"
    _imagem2 = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Kittens_resting_close_together_for_warmth_and_security.jpg/1920px-Kittens_resting_close_together_for_warmth_and_security.jpg"
    _imagem3 = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Domestic_Cat_Face_Shot.jpg/1920px-Domestic_Cat_Face_Shot.jpg"
    _imagem4 = "https://impa.br/wp-content/uploads/2025/04/IMG_6669-1-1200x900.png"

    _set_imagens_1 = [_imagem1]
    _set_imagens_2 = [_imagem1, _imagem2]
    _set_imagens_3 = [_imagem1, _imagem2, _imagem3]
    _set_imagens_4 = [_imagem4]

    # Nota para Erique: Implementar configuração de disposição de imagem e texto nos balões (layouts)
    # Implementar dimensionamento dinâmico de imagens nos balões
    # Fazer o balão permanecer quando o mouse está sobre ele

    lorem_ipsum = "is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
    lorem_ipsum_source = "https://www.lipsum.com/"

    bottom_events = [
        (-400, 0, None, f"<a href = {lorem_ipsum_source}>Lorem Ipsum</a>" + " " + lorem_ipsum, "#cc0066"),
        (-380, 10, _set_imagens_1, f"<a href = {lorem_ipsum_source}>Lorem Ipsum</a>" + " " + lorem_ipsum, "#ff9100"),
        (-360, 20, None, f"<a href = {lorem_ipsum_source}>Lorem Ipsum</a>" + " " + lorem_ipsum, "#00ffff"),
        (-340, 30, _set_imagens_2, f"<a href = {lorem_ipsum_source}>Lorem Ipsum</a>" + " " + lorem_ipsum, "#6f00ff"),
        (-320, 0, None, f"<a href = {lorem_ipsum_source}>Lorem Ipsum</a>" + " " + lorem_ipsum, "#008800"),
        (-300, 10, _set_imagens_3, f"<a href = {lorem_ipsum_source}>Lorem Ipsum</a>" + " " + lorem_ipsum, "#ffffff"),
        (-280, 20, None, f"<a href = {lorem_ipsum_source}>Lorem Ipsum</a>" + " " + lorem_ipsum, "#ffee07"),
        (-260, 30, _set_imagens_1, f"<a href = {lorem_ipsum_source}>Lorem Ipsum</a>" + " " + lorem_ipsum, "#ff0883"),
        (-200, 0, None, f"<a href = {lorem_ipsum_source}>Lorem Ipsum</a>" + " " + lorem_ipsum, "#ff0000"),
        (-200, 30, _set_imagens_2, f"<a href = {lorem_ipsum_source}>Lorem Ipsum</a>" + " " + lorem_ipsum, "#ffee00"),
        (-200, 60, None, f"<a href = {lorem_ipsum_source}>Lorem Ipsum</a>" + " " + lorem_ipsum, "#7afd00"),
        (2004, 0, _set_imagens_4, "2004: Nasce o proeminente matemático Vitor Hugo de Souza.", "#60ff03"),
        (1980, 0, None, "1980: Morre John Lennon.", "#00f7ff")
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

from flask import Flask, render_template_string
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Linha do Tempo</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.26.0/cytoscape.min.js"></script>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #121212;
            color: #ccc;
            font-family: sans-serif;
            overflow-y: hidden;
        }
        .scroll-wrapper {
            width: 100vw;
            height: 100vh;
            overflow-x: auto;
            position: relative;
        }
        .epoch-line {
            position: absolute;
            top: 0;
            bottom: 0;
            width: 1px;
            background-color: rgba(255, 255, 255, 0.1);
            border-left: 1px dashed rgba(255, 255, 255, 0.15);
            z-index: 0;
            pointer-events: none;
        }
        .epoch-label {
            position: absolute;
            top: 20px;
            transform: translateX(-50%);
            font-size: 14px;
            color: #666;
            font-weight: bold;
            letter-spacing: 1px;
            text-transform: uppercase;
            z-index: 0;
            pointer-events: none;
        }
        #cy {
            height: 100vh;
            width: {{ total_width }}px;
            position: absolute;
            top: 0;
            left: 0;
            z-index: 1;
        }
        #instrucoes {
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: rgba(0,0,0,0.8);
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid #333;
            z-index: 10;
            color: #8ab4f8;
        }
    </style>
</head>
<body>
    <div class="scroll-wrapper">
        {% for epoch in epochs %}
        <div class="epoch-line" style="left: {{ epoch.x }}px;"></div>
        <div class="epoch-label" style="left: {{ epoch.x }}px;">{{ epoch.label }} ({{ epoch.year }})</div>
        {% endfor %}
        <div id="cy"></div>
    </div>

    <script>
        var elements = {{ elements_json | safe }};
        
        var cy = cytoscape({
            container: document.getElementById('cy'),
            elements: elements,
            zoomingEnabled: false,
            panningEnabled: false,
            boxSelectionEnabled: false,

            style: [
                {
                    selector: 'node',
                    style: {
                        'shape': 'round-rectangle',
                        'width': 'data(width)',
                        'height': 40,
                        'background-color': 'rgba(138, 180, 248, 0.05)',
                        'border-width': 1,
                        'border-color': 'rgba(138, 180, 248, 0.4)',
                        'label': 'data(id)',
                        'color': '#8ab4f8', 
                        'font-size': '18px',
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'font-family': 'monospace',
                        'text-color': '#000000'
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'width': 2.5,
                        'line-color': 'data(targetColor)',
                        'target-arrow-color': 'data(targetColor)',
                        'target-arrow-shape': 'triangle',
                        
                        /* Configuração para Curva de 90° Suavizada */
                        'curve-style': 'taxi', 
                        'taxi-direction': 'rightward', /* Força o fluxo da esquerda para a direita */
                        'taxi-radius': 30, /* Cria o arredondamento na quina de 90 graus */
                        'edge-distances': 'node-position'
                    }
                },
                {
                    selector: '.timeline-edge',
                    style: {
                        'line-color': 'data(targetColor)',
                        'target-arrow-color': 'data(targetColor)',
                        'line-style': 'dashed',
                        'width': 1.5,
                        
                        'curve-style': 'taxi',
                        'taxi-direction': 'rightward',
                        'taxi-radius': 30,
                        'edge-distances': 'node-position',
                        'opacity': 0.6
                    }
                }
            ],
            layout: {
                name: 'preset' 
            }
        });
    </script>
</body>
</html>
"""

def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"

@app.route('/')
def index():
    nodes = [
        ("Comida", -600, -300, "#88CC88"),
        ("Bacon", -290, 600, "#ddcc44"),
        ("Calabresa", -280, 610, "#cc4466") 
    ]

    bifurcations = [
        ("Comida", "Bacon"),
        ("Comida", "Calabresa")
    ]

    y_tracks = {
        "Comida": 0, "Bacon": -120, "Calabresa": 120
    }

    color_map = {node[0]: node[3] for node in nodes}
    node_metrics = {}

    epsilon = 200
    min_year = -700 - epsilon
    max_year = 2026 + epsilon
    scale_x = 3.5
    total_width = (max_year - min_year) * scale_x
    base_y = 400

    elements = []
    gap_px = 16 
    for name, start_y, end_y, color in nodes:
        duration = end_y - start_y
        mid_year = start_y + (duration / 2)
        x_pos = (mid_year - min_year) * scale_x
        width_px = (duration * scale_x) - gap_px
        
        if width_px < 150: 
            width_px = 150

        y_pos = base_y + y_tracks.get(name, 0)
        node_metrics[name] = {
            'start_y': start_y,
            'end_y': end_y,
            'x_pos': x_pos
        }
        
        elements.append({
            "data": {
                "id": name, 
                "width": width_px
            },
            "position": {"x": x_pos, "y": y_pos},
            "style": {
                "background-color": hex_to_rgba(color, 0.12),
                "border-color": hex_to_rgba(color, 0.6),
                "color": color,           
                "text-color": color       
            }
        })
        
    def new_edge(src, tgt, timeline_class=False):
        tgt_color = color_map.get(tgt, '#555')
        src_info = node_metrics.get(src)
        tgt_info = node_metrics.get(tgt)
        
        taxi_turn_px = 0
        if src_info and tgt_info:
            turn_year = tgt_info['start_y'] - 20
            if turn_year <= src_info['end_y']:
                turn_year = src_info['end_y'] + 5 
            turn_x = (turn_year - min_year) * scale_x
            taxi_turn_px = turn_x - src_info['x_pos']

        edge_element = {
            "data": {
                "source": src, 
                "target": tgt,
                "targetColor": tgt_color
            },
            "style": {
                "taxi-turn": f"{taxi_turn_px}px"
            }
        }
        
        if timeline_class:
            edge_element["classes"] = "timeline-edge"
            
        elements.append(edge_element)

    for src, tgt in bifurcations:
        new_edge(src, tgt)

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

    for epoch in historical_epochs:
        epoch['x'] = (epoch['year'] - min_year) * scale_x

    return render_template_string(
        HTML_TEMPLATE, 
        elements_json=json.dumps(elements),
        epochs=historical_epochs,
        total_width=total_width
    )

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
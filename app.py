from flask import Flask, render_template
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
    
    # Nome, ano inicial, ano final, cor
    
    nodes = {
        "Comida": (-600, -300, "#88CC88"),
        "Bacon":(-290, 600, "#ddcc44"),
        "Calabresa": (-280, 610, "#cc4466") 
    }

    bifurcations = [
        ("Comida", "Bacon"),
        ("Comida", "Calabresa")
    ]

    y_tracks = {
        "Comida": 0, "Bacon": -120, "Calabresa": 120
    }
    
    # nodes[2][3]
    
    # Nome, ano, ofsetY, img, linha de pensamento

    philosophers = [
        ("Francis Bacon", 350, -200, 'Bacon.png', "Bacon"), 
        ("Francis Calabresa", 400, 200, "Calabresa.png", "Calabresa"),
        ('Francis Brioche', -560, 75, 'Brioche.png', 'Comida'),
        ('Francis Pretzel', -370, 150, 'Pretzel.png', 'Comida') 
    ]
    
    # Origem, Destino, Descrição
    
    # A criticou B
    
    criticism_target = {
        'Francis Bacon': ('Francis Calabresa', 'Bacon é melhor do que Calabresa!'),
        'Francis Calabresa': ('Francis Bacon', 'Bacon faz mal a saúde!'),
    }
    
    # B foi criticado por A
    
    criticism_origin = {
        'Francis Bacon': ('Francis Calabresa', 'Bacon tem muita gordura!'),
        'Francis Calabresa': ('Francis Bacon', 'Calabresa mata a alma!'),
    }
    
    agreement_target = {
    }
    
    agreement_origin = {
    }

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

    # Renderização
    
    color_map = {}; node_metrics = {}
    for name in nodes.keys():
        color_map[name] = nodes[name][2]

    epsilon = 200
    min_year = -700 - epsilon
    max_year = 2026 + epsilon
    scale_x = 3.5
    total_width = (max_year - min_year) * scale_x
    base_y = 400

    elements = []
    gap_px = 16 
    for name in nodes.keys():
        start_y, end_y, color = nodes[name]
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
                "width": width_px,
                
            },
            "position": {"x": x_pos, "y": y_pos},
            "style": {
                "background-color": hex_to_rgba(color, 0.12),
                "border-color": hex_to_rgba(color, 0.6),
                "color": color,           
                "text-color": color       
            }
        })
        
        
    # Filósofos
    
    def add_philosopher(name, year_x, offset_y, img_file, idea):
        x_pos = (year_x - min_year) * scale_x
        
        y_pos = base_y + offset_y

        elements.append({
            "data": {
                "id": name,
                "image": f"/static/img/{img_file}",
                "criticism_t": criticism_target.get(name, None),
                "criticism_o": criticism_origin.get(name, None),
                "agreement_t": agreement_target.get(name, None),
                "agreement_o": agreement_origin.get(name, None),
            },
            'style':{
                'border-color': hex_to_rgba(nodes[idea][2], 1),
            },
            "position": {"x": x_pos, "y": y_pos},
            "classes": "philosopher"
        })

    for name, year_x, offset_y, img_file, idea in philosophers:
        add_philosopher(name, year_x, offset_y, img_file, idea)
        
    def new_edge(src, tgt):
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
        elements.append(edge_element)

    for src, tgt in bifurcations:
        new_edge(src, tgt)

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
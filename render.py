def hex_to_rgba(hex_color, alpha, factor=1):
    """Conversão de Hex para RGBA com argumento adicional factor de clareamento"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return f"rgba({r}, {g}, {b}, {alpha})"

def general_metrics(philosophies):
    """Calcula o grid básico, posições e metadados das correntes filosóficas"""
    # Eixo X
    epsilon = 200
    min_year = -700 - epsilon
    max_year = 2026 + epsilon
    scale_x = 1.5
    total_width = (max_year - min_year) * scale_x
    
    # Eixo Y
    total_height = 1000 
    timeline_center = total_height * 0.4
    events_center = total_height * 0.9
    
    philosophy_metrics = {}
    for name, values in philosophies.items():
        start_year, end_year, y_offset, color = values
        
        duration = end_year - start_year
        mid_year = start_year + (duration / 2)
        
        x_pos = (mid_year - min_year) * scale_x
        height_px = 3; gap_px = 3
        width_px = max(150, (duration * scale_x) + gap_px)        
        y_pos = timeline_center + y_offset
        
        philosophy_metrics[name] = {
            'start_year': start_year, 
            'end_year': end_year,
            'x_pos': x_pos,
            'y_pos': y_pos,
            'width_px': width_px,
            'height_px': height_px,
            'color': color
        }
    return min_year, scale_x, total_width, total_height, timeline_center, events_center, philosophy_metrics

def build_epochs(epochs, min_year, scale_x):
    """Calcula a posição X (em pixels) para as marcações de época."""
    epoch_markers = []
    
    for year, label in epochs:
        x_pos = (year - min_year) * scale_x
        epoch_markers.append({
            "year": year,
            "label": label,
            "x_pos": x_pos
        })
    return epoch_markers

def build_philosophies(philosophy_metrics, bifurcations, min_year, scale_x):
    """Gera os elementos das correntes principais (nós) e suas ramificações (arestas)."""
    elements = []
    
    # Construção das Correntes Filosóficas
    for name, metric in philosophy_metrics.items():
        color = metric['color']
        elements.append({
            "classes": "philosophy",
            "data": {
                "id": name, 
                "width": metric['width_px'],
                "height": metric['height_px']
            },
            "position": {"x": metric['x_pos'], "y": metric['y_pos']},
            "style": {
                "background-color": hex_to_rgba(color, 0.12),
                "border-color": hex_to_rgba(color, 0.6),
                "color": color   
            }
        })
        
    # Construção das Bifurcações
    for src, tgt in bifurcations:
        src_info = philosophy_metrics.get(src)
        tgt_info = philosophy_metrics.get(tgt)
        tgt_color = tgt_info['color']
        
        # Vértice Invisível em Source
        delta_year = 40
        branch_year = tgt_info['start_year'] - delta_year
        branch_x = (branch_year - min_year) * scale_x
        branch_y = src_info['y_pos']
        inv_src_id = f"anchor_{src}_to_{tgt}"
        
        elements.append({
            "data": {"id": inv_src_id},
            "position": {"x": branch_x, "y": branch_y},
            "style": {"width": 1, "height": 1, "opacity": 0, "events": "no"}
        })
        
        # Vértice Invisível em Target
        arrival_x = (tgt_info['start_year'] - min_year) * scale_x
        arrival_y = tgt_info['y_pos']
        inv_tgt_id = f"anchor_{tgt}_from_{src}"
        
        elements.append({
            "data": {"id": inv_tgt_id},
            "position": {"x": arrival_x, "y": arrival_y},
            "style": {"width": 1, "height": 1, "opacity": 0, "events": "no"}
        })

        # Aresta ligando as correntes filosóficas
        elements.append({
            "classes": "philosophy",
            "data": {
                "id": f"edge_branch_{src}_{tgt}",
                "source": inv_src_id, 
                "target": inv_tgt_id,
                "targetColor": tgt_color
            }
        })
    return elements

def build_circle_node(node_id, x, y, size, color, classes="", img_url=None, label="", border_width=2):
    """Abstração de um nó circular. Serve tanto para filósofos quanto eventos."""

    # Propriedades Gerais Dinâmicas
    final_classes = f"circle-node {classes}".strip()
    data_dict = {
        "id": node_id, 
        "label": label
    }
    style = {
        "width": size,
        "height": size,
        "border-width": border_width,
        "border-color": color
    }

    # Visibilidade por Cor ou Imagem
    if img_url:
        data_dict["img"] = img_url 
    else:
        style["background-color"] = hex_to_rgba(color, 1) if color.startswith('#') else color

    return {
        "classes": final_classes,
        "data": data_dict, 
        "position": {"x": x, "y": y},
        "style": style
    }

def build_rect_node(node_id, x, y, width, height, color, classes="", label="", border_width=0, z_index=9, font_size=11, font_color="#000000", font_family="sans-serif"):
    """Abstração dos elementos retangulares da UI."""

    final_classes = f"rect-node {classes}".strip()
    return {
        "classes": final_classes,
        "data": {"id": node_id, "label": label},
        "position": {"x": x, "y": y},
        "style": {
            "width": width,
            "height": height,
            "background-color": color,
            "border-width": border_width,
            "z-index": z_index,
            "font-size": font_size,
            "color": font_color,
            "font-family": font_family,
            "text-wrap": "wrap",
            "text-max-width": width - 16,
            "padding": 2
        }
    }

def build_events(events, min_year, scale_x, events_center):
    """Constroi os eventos históricos da linha do tempo."""
    
    elements = []
    SHOW_NAMES = False
    CARD_WIDTH = 260
    SUMMARY_HEIGHT = 70

    for i, (year, y_offset, img, label, tooltip, color) in enumerate(events):
        # Evento
        x_pos = (year - min_year) * scale_x
        y_pos = events_center + y_offset
        
        event_id = f"event_{i}"
        event_node = build_circle_node(
            node_id=event_id,
            x=x_pos,
            y=y_pos,
            size=30,
            color=color,
            classes="event",
            img_url=img,
            label=label if SHOW_NAMES else "",
            border_width=2
        )
        event_node["data"]["event_id"] = event_id
        event_node["data"]["tooltip"] = tooltip
        if img:
            event_node["data"]["imgUrls"] = [img]
            
        elements.append(event_node)

        # Interface
        detail_class = f"event-detail details_{event_id}"
        card_y = y_pos - 75
        summary_id = f"summary_{event_id}"
        summary_node = build_rect_node(
            node_id=summary_id,
            x=x_pos, y=card_y,
            width=CARD_WIDTH, 
            height="label",
            color="#d9d9d9", 
            classes=detail_class,
            label=f"{label}\n\n{tooltip}",
            border_width=4,
            font_size=12,
            font_color="#222222", 
            font_family="monospace"
        )
        summary_node["style"]["border-color"] = color
        elements.append(summary_node)

        # Ligação
        elements.append({
            "classes": detail_class + " dashed-link",
            "data": {
                "id": f"edge_{event_id}_{summary_id}", 
                "source": event_id, 
                "target": summary_id
            }
        })
    return elements

def build_philosophers(philosophers, philosophy_metrics, min_year, scale_x):
    """Constroi a informação completa dos nós que representam os filósofos"""

    elements = []
    SHOW_NAMES = True
    CARD_WIDTH = 260
    BUTTON_HEIGHT = 26
    GAP_SUMMARY = 0
    GAP_BUTTONS = 12
    PORTRAIT_RADIUS = 27.5
    GAP_TO_CARD = 30
    
    def get_direction_sign(y_position):
        return 1 if y_position <= 500 else -1

    for name, philosophy, year, offset, img, info in philosophers:
        line_info = philosophy_metrics.get(philosophy) 
        if not line_info: 
            continue
            
        x_pos = (year - min_year)*scale_x
        y_pos_line = line_info['y_pos'] + offset
        sign = get_direction_sign(y_pos_line)

        # Botão Geral do Filósofo
        safe_name = name.lower().replace(' ', '_')
        phil_id = f"phil_{safe_name}"
        phil_node = build_circle_node(
            node_id=phil_id,
            x=x_pos,
            y=y_pos_line,
            size=55,
            color=line_info['color'],
            classes="phil-portrait",
            img_url=img,
            label=name if SHOW_NAMES else "",
            border_width=3
        )
        phil_node["data"]["phil_name"] = name
        elements.append(phil_node)

        text_content = f"{name}\n\n{info}"
        chars_per_line = 34
        lines = 0
        for paragraph in text_content.split('\n'):
            if paragraph == "":
                lines += 1
            else:
                lines += (len(paragraph) + chars_per_line - 1) // chars_per_line
        estimated_card_height = max(70, (lines * 15) + 20) 

        # Variáveis para Stacking dos Botões
        dist_to_card_center = PORTRAIT_RADIUS + GAP_TO_CARD + (estimated_card_height / 2)
        card_y = y_pos_line + (sign * dist_to_card_center)

        detail_class = f"phil-detail details_{safe_name}"
        button_class = f"clickable-button details_{safe_name}"
        summary_id = f"summary_{safe_name}"

        # Resumo
        summary_node = build_rect_node(
            node_id=summary_id,
            x=x_pos, y=card_y,
            width=CARD_WIDTH, height="label",
            color="#d9d9d9", 
            classes=detail_class,
            label=text_content,
            border_width=4,
            font_size=12,
            font_color="#222222", 
            font_family="monospace" 
        )
        summary_node["style"]["border-color"] = line_info['color']
        elements.append(summary_node)

        # Ligação
        elements.append({
            "classes": detail_class + " dashed-link",
            "data": {"source": phil_id, "target": summary_id}
        })

        # Botões
        dist_to_first_btn = (estimated_card_height / 2) + GAP_SUMMARY + (BUTTON_HEIGHT / 2)
        current_btn_y = card_y + (sign * dist_to_first_btn)

        btn_labels = [
            ("Filósofos contrários", "#ff6666"),
            ("Filósofos adeptos", "#66cc66"),
            ("Influenciados", "#6688ff"),
            ("Principais obras", "#aa88cc")
        ]

        for i, (btn_text, btn_color) in enumerate(btn_labels):
            elements.append(build_rect_node(
                node_id=f"btn_{safe_name}_{i}",
                x=x_pos, y=current_btn_y,
                width=CARD_WIDTH, height=BUTTON_HEIGHT,
                color=btn_color,
                classes=button_class,
                label=btn_text,
                z_index=11
            ))
            current_btn_y += sign * (BUTTON_HEIGHT + GAP_BUTTONS)
            
    return elements

def build_timeline_elements(data):
    """Função principal de construção da timeline."""

    # Extração de Dados
    epochs = data.get('epochs', [])
    events = data.get('events', [])
    philosophies = data.get('philosophies', {})
    bifurcations = data.get('bifurcations', [])
    philosophers = data.get('philosophers', [])

    # Métricas Base
    min_year, scale_x, total_width, total_height, timeline_center, events_center, philosophy_metrics = general_metrics(philosophies)

    # Marcação de Épocas
    epoch_markers = build_epochs(epochs, min_year, scale_x)
    
    # Construção dos Elementos
    elements = []
    elements.extend(build_philosophies(philosophy_metrics, bifurcations, min_year, scale_x))
    elements.extend(build_philosophers(philosophers, philosophy_metrics, min_year, scale_x))
    elements.extend(build_events(events, min_year, scale_x, events_center))

    return {
        "elements": elements,
        "epochs": epoch_markers,
        "total_width": total_width,
        "total_height": total_height,
        "min_year": min_year,
        "scale_x": scale_x
    }
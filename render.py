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
                "color": color,           
                "text-color": color       
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
                "source": inv_src_id, 
                "target": inv_tgt_id,
                "targetColor": tgt_color
            }
        })
        
    return elements

def build_timeline_elements(data):
    """Função principal de construção da timeline."""

    # Extração de Dados
    philosophies = data.get('philosophies', {})
    bifurcations = data.get('bifurcations', [])
    epochs = data.get('epochs', [])
    
    # Métricas Base
    min_year, scale_x, total_width, total_height, timeline_center, events_center, philosophy_metrics = general_metrics(philosophies)

    # Marcação de Épocas
    epoch_markers = build_epochs(epochs, min_year, scale_x)
    
    # Construção dos Elementos
    elements = []
    elements.extend(build_philosophies(philosophy_metrics, bifurcations, min_year, scale_x))

    return {
        "elements": elements,
        "epochs": epoch_markers,
        "total_width": total_width,
        "total_height": total_height,
        "min_year": min_year,
        "scale_x": scale_x
    }
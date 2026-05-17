def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"

def build_timeline_elements(nodes, bifurcations, y_tracks):
    color_map = {node[0]: node[3] for node in nodes}
    node_metrics = {}

    epsilon = 200
    min_year = -700 - epsilon
    max_year = 2026 + epsilon
    scale_x = 1.5
    total_width = (max_year - min_year) * scale_x
    base_y = 400

    elements = []
    gap_px = -3
    
    # Nós (Linhas de Pensamento)
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
            'x_pos': x_pos,
            'y_pos': y_pos 
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
        
    # Arestas (Ligações entre Nós)
    def new_edge(src, tgt):
        tgt_color = color_map.get(tgt, '#555')
        src_info = node_metrics.get(src)
        tgt_info = node_metrics.get(tgt)
        
        if not (src_info and tgt_info):
            return
            
        branch_year = tgt_info['start_y'] - 50
        branch_x = (branch_year - min_year) * scale_x
        branch_y = src_info['y_pos']
        inv_src_id = f"anchor_{src}_to_{tgt}"
        
        elements.append({
            "data": {"id": inv_src_id},
            "position": {"x": branch_x, "y": branch_y},
            "style": {
                "width": 1,
                "height": 1,
                "opacity": 0,
                "events": "no"
            }
        })
        
        tgt_start_x = (tgt_info['start_y'] - min_year) * scale_x
        tgt_start_y = tgt_info['y_pos']
        inv_tgt_id = f"anchor_{tgt}_from_{src}"
        
        elements.append({
            "data": {"id": inv_tgt_id},
            "position": {"x": tgt_start_x, "y": tgt_start_y},
            "style": {
                "width": 1,
                "height": 1,
                "opacity": 0,
                "events": "no"
            }
        })

        edge_element = {
            "data": {
                "source": inv_src_id, 
                "target": inv_tgt_id,
                "targetColor": tgt_color
            }
        }
        elements.append(edge_element)

    for src, tgt in bifurcations:
        new_edge(src, tgt)

    return elements, total_width, min_year, scale_x
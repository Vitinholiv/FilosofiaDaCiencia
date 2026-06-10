# Adição do argumento factor com defalt 1
# factor < 1 são usados na borda dos círculos de bottom_events, a cor fica levemente mais escura que hex_color
def hex_to_rgba(hex_color, alpha, factor=1):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return f"rgba({r}, {g}, {b}, {alpha})"

def build_timeline_elements(nodes, bifurcations, y_tracks, bottom_events=[], philosophers=[]):
    color_map = {}; node_metrics = {}
    for name in nodes.keys():
        color_map[name] = nodes[name][2]

    epsilon = 200
    min_year = -700 - epsilon
    max_year = 2026 + epsilon
    scale_x = 1.5
    total_width = (max_year - min_year) * scale_x
    base_y = 400
    bottom_y = base_y + 200 # Posição dos círculos 

    elements = []
    gap_px = -3
    
    # Nós (Linhas de Pensamento)
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


    # ==========================================
    # NOVO CÓDIGO: CARD DOS FILÓSOFOS
    # ==========================================
    
    for name, year, offset, img, info, btn_data in philosophers:
        
        card_offset = 85
        btn_offset = 55
        btn_up = 32

        # Para que as caixas fiquem na tela
        
        if offset > 120:
            card_offset = -85
            btn_offset = -55
            btn_up = -32

        
        line_info = node_metrics.get("Bacon")
        if not line_info: continue
        
        x_pos = (year - min_year) * scale_x
        y_pos_line = line_info['y_pos'] + offset
        
        # Criamos as classes para o JS controlar
        detail_class = f"phil-detail details_{name.replace(' ', '_')}"
        
        # A) Retrato do Filósofo (na linha principal)
        portrait_id = f"phil_{name}"
        elements.append({
            "classes": "phil-portrait",
            "data": {"id": portrait_id, "label": name, "phil_name": name},
            "position": {"x": x_pos, "y": y_pos_line},
            "style": {
                "shape": "ellipse",
                "width": 55,
                "height": 55,
                "z-index": 8,
                "background-color": "#fff",
                "border-width": 3,
                "border-color": "#ddcc44",
                "background-image": img,
                "background-fit": "cover",
                "label": "Clicar no filósofo " + name,
                "text-valign": "bottom",
                "text-margin-y": 8,
                "font-size": 11,
                "font-weight": "bold",
                "color": "#333",
                "text-wrap": "wrap"
            }
        })
        
        # B) Caixa de Resumo
        card_y = y_pos_line + card_offset
        info_id = info 
        elements.append({
            "classes": detail_class,
            "data": {
                "id": info_id, 
                "label": f"{name} (1561–1626)\n\nFilósofo empirista."
            },
            "position": {"x": x_pos, "y": card_y},
            "style": {
                "shape": "round-rectangle",
                "width": 260,
                "height": 70,
                "z-index": 9,
                "background-color": "#d9d9d9",
                "color": "#000",
                "text-valign": "center",
                "text-halign": "center",
                "text-wrap": "wrap",
                "font-size": 11,
                "border-width": 0,
                "border-top-width": 20,
                "border-color": "#ddcc44"
            }
        })
        
        # Linha pontilhada
        elements.append({
            "classes": detail_class,
            "data": {"source": portrait_id, "target": info_id},
            "style": {
                "width": 2,
                "line-color": "#b3b3b3",
                "line-style": "dashed",
                "target-arrow-shape": "none"
            }
        })
        
        btn_y = card_y + btn_offset
        
        # Background preto atrás dos botões
        elements.append({
            "classes": detail_class,
            "position": {"x": x_pos, "y": btn_y + (btn_up * 1.5)}, 
            "data": {"id": f"btn_bg_{name}", "label": "",},
            "style": {
                "shape": "round-rectangle",
                "width": 260,
                "height": abs(btn_up) * 4 + 20,  
                "background-color": "#000000",
                "border-width": 2,
                "border-color": "#888888",
                "z-index": 10,  
                "label": "",
                "color": "transparent"
            }
        })
        
        # C) Botões Coloridos
        
        buttons = [
            ("Filósofos contrários", "#ff6666", btn_data.get("Contrários", [])),
            ("Filósofos adeptos",    "#66cc66", btn_data.get("Adeptos", [])),
            ("Influenciados",        "#6688ff", btn_data.get("Influenciados", {"Concorda": [], "Discorda": []})),
            ("Principais obras",     "#aa88cc", btn_data.get("Obras", []))
        ]
        
        
        for i, (btn_text, btn_color, btn_items) in enumerate(buttons):
            elements.append({
                "classes": detail_class,
                "data": {"id": f"btn_{name}_{i}", "label": btn_text, 'items': btn_items}, 
                "position": {"x": x_pos, "y": btn_y},
                "style": {
                    "shape": "round-rectangle",
                    "width": 240,
                    "height": 26,
                    "z-index": 11,
                    "background-color": btn_color,
                    "color": "#000",
                    "text-valign": "center",
                    "text-halign": "center",
                    "font-size": 11,
                    "font-weight": "bold",
                    "label": btn_text,  
                }
            })
            
            btn_y += btn_up









    # Eventos Históricos e Trabalhos
    for i, (year, row_offset, img_url, text, color) in enumerate(bottom_events):
        x_pos = (year - min_year) * scale_x
        y_pos = bottom_y + row_offset

        node_data = {
            "id": f"bottom_event_{i}",
            "tooltip": text
        }

        if img_url:
            node_data["img_urls"] = img_url

        elements.append({
            "classes": "bottom-event",
            "data": node_data,
            "position": {"x": x_pos, "y": y_pos},
            "style": {
                "background-color": hex_to_rgba(hex_color=color, alpha=1, factor=1),
                "border-color": hex_to_rgba(hex_color=color, alpha=1, factor=0.5)   # A borda dos círculos é 50% mais escura que a cor do interior
            }
        })

    return elements, total_width, min_year, scale_x

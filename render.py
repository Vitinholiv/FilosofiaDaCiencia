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

def general_metrics(philosophies, events_band_height=70):
    """Calcula o grid básico, posições e metadados das correntes filosóficas"""
    # Eixo X
    epsilon = 20
    min_year = 1600 - epsilon
    max_year = 2026 + epsilon
    scale_x = 10
    total_width = (max_year - min_year) * scale_x

    # Eixo Y
    total_height = 1000
    timeline_center = total_height * 0.4
    # A faixa fica com metade da sua altura acima e metade abaixo de events_center;
    # para colar exatamente na borda inferior da página, o centro precisa ficar
    # deslocado de total_height por meia altura da faixa.
    events_center = total_height - (events_band_height / 2)

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
        delta_year = 5
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

def build_rect_node(node_id, x, y, width, height, color, classes="", label="", border_width=0, z_index=9, font_size=11, font_color="#000000", font_family="sans-serif", bg_opacity=None, border_opacity=None):
    """Abstração dos elementos retangulares da UI.

    IMPORTANTE: o Cytoscape.js ignora o canal alpha de strings rgba() passadas em
    'background-color'/'border-color' — a opacidade real é controlada pelas propriedades
    separadas 'background-opacity'/'border-opacity' (padrão 1). Por isso, quando `color`
    já vier como rgba(...) com alpha < 1 (ex.: gerado por hex_to_rgba), é necessário também
    informar bg_opacity/border_opacity explicitamente, ou a opacidade é perdida.
    """

    final_classes = f"rect-node {classes}".strip()
    style = {
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
    if bg_opacity is not None:
        style["background-opacity"] = bg_opacity
    if border_opacity is not None:
        style["border-opacity"] = border_opacity

    return {
        "classes": final_classes,
        "data": {"id": node_id, "label": label},
        "position": {"x": x, "y": y},
        "style": style
    }

def build_events_band(events_center, band_height, band_color, band_opacity, border_opacity,
                       total_width, staff, staff_lines, staff_opacity, staff_color):
    """Constrói a faixa de eventos (fundo, bordas e linhas de partitura) como elementos reais
    do grafo do Cytoscape, ao invés de divs HTML sobrepostas. Assim a ordem de empilhamento
    entre a faixa e os nós (eventos, filósofos etc.) é resolvida pelo próprio Cytoscape:
    esses elementos usam z-index 0 e são inseridos antes dos demais, então ficam atrás de
    tudo que tiver z-index igual (o padrão), sem cobrir nem ser coberto de forma inconsistente."""
    elements = []
    cx = total_width / 2

    # Fundo translúcido da faixa
    # (band_color aqui é passado "cru", sem alpha embutido; a opacidade vai explicitamente
    # em bg_opacity, já que o Cytoscape ignora o alpha de rgba() em background-color)
    bg = build_rect_node(
        node_id="events-band-bg",
        x=cx, y=events_center,
        width=total_width, height=band_height,
        color=band_color,
        classes="events-band-bg",
        border_width=0, z_index=0,
        bg_opacity=band_opacity
    )
    bg["style"]["events"] = "no"
    elements.append(bg)

    # Bordas superior e inferior
    for suffix, edge_y in (("top", events_center - band_height / 2), ("bottom", events_center + band_height / 2)):
        border = build_rect_node(
            node_id=f"events-band-border-{suffix}",
            x=cx, y=edge_y,
            width=total_width, height=0.2,
            color=band_color,
            classes="events-band-border",
            border_width=0, z_index=0,
            bg_opacity=border_opacity
        )
        border["style"]["events"] = "no"
        elements.append(border)

    # Linhas de partitura (opcional)
    if staff:
        n = staff_lines or 5
        spacing = band_height / (n + 1)
        line_color = staff_color or band_color
        top = events_center - band_height / 2

        for i in range(1, n + 1):
            y = top + spacing * i
            line = build_rect_node(
                node_id=f"events-band-staff-{i}",
                x=cx, y=y,
                width=total_width, height=1,
                color=line_color,
                classes="events-band-staff-line",
                border_width=0, z_index=0,
                bg_opacity=staff_opacity
            )
            line["style"]["events"] = "no"
            elements.append(line)

    return elements

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
            size=25,
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

def build_philosopher_card_html(name, info, border_color):
    """Monta o HTML em tópicos exibido sobre o card de resumo do filósofo.

    `info` é uma lista de (título, conteúdo), onde conteúdo é uma string
    (tópico simples) ou uma lista de strings (subtópicos)."""
    topics = []
    for title, content in info:
        if isinstance(content, (list, tuple)):
            sub = "".join(f"<li>{item}</li>" for item in content)
            topics.append(f"<li><b>{title}:</b><ul>{sub}</ul></li>")
        else:
            topics.append(f"<li><b>{title}:</b> {content}</li>")
    return (
        f'<div class="phil-card" style="border-color:{border_color}">'
        f'<div class="phil-card-name">{name}</div>'
        f'<ul class="phil-topics">{"".join(topics)}</ul>'
        f'</div>'
    )

def estimate_info_height(info, chars_per_line=34, line_h=17, pad=52):
    """Estima a altura do card estruturado para posicionar botões e o nó âncora."""
    lines = 1  # linha do nome
    for title, content in info:
        if isinstance(content, (list, tuple)):
            head = f"{title}:"
            lines += max(1, (len(head) + chars_per_line - 1) // chars_per_line)
            for item in content:
                lines += max(1, (len(item) + chars_per_line - 1) // chars_per_line)
        else:
            head = f"{title}: {content}"
            lines += max(1, (len(head) + chars_per_line - 1) // chars_per_line)
    return max(70, lines * line_h + pad)

def build_side_card_html(header_text, body_text, color):
    """HTML de um card lateral dos botões (cabeçalho colorido + corpo); altura automática via CSS."""
    header_bg = hex_to_rgba(color, 0.3)
    body_html = "<br>".join(body_text.split("\n"))
    return (
        f'<div class="side-card" style="border-color:{color}">'
        f'<div class="side-card-header" style="background-color:{header_bg};border-bottom-color:{color}">{header_text}</div>'
        f'<div class="side-card-body">{body_html}</div>'
        f'</div>'
    )

def build_philosophers(philosophers, philosophy_metrics, min_year, scale_x, works=None, influences=None, adepts=None, oppositions=None):
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

        card_html = build_philosopher_card_html(name, info, line_info['color'])
        estimated_card_height = estimate_info_height(info)

        detail_class = f"phil-detail details_{safe_name}"
        button_class = f"clickable-button details_{safe_name}"
        summary_id = f"summary_{safe_name}"

        # Card de descrição + botões: coluna à ESQUERDA da bolinha, centralizada
        # verticalmente na altura do filósofo (evita que o card vaze da tela).
        GAP_CARD_BUTTONS = 25
        buttons_block_h  = 4 * BUTTON_HEIGHT + 3 * GAP_BUTTONS
        group_height     = estimated_card_height + GAP_CARD_BUTTONS + buttons_block_h
        group_top        = y_pos_line - (group_height / 2)

        left_x = x_pos - (PORTRAIT_RADIUS + GAP_TO_CARD + (CARD_WIDTH / 2))
        card_y = group_top + (estimated_card_height / 2)

        # Resumo (nó âncora transparente; o conteúdo visível é o overlay HTML)
        summary_node = build_rect_node(
            node_id=summary_id,
            x=left_x, y=card_y,
            width=CARD_WIDTH, height=estimated_card_height,
            color="rgba(0,0,0,0)",
            classes=detail_class,
            label="",
            border_width=0
        )
        summary_node["data"]["html"] = card_html
        elements.append(summary_node)

        # Ligação bolinha -> card
        elements.append({
            "classes": detail_class + " dashed-link",
            "data": {"source": phil_id, "target": summary_id}
        })

        # Botões: empilhados abaixo do card, na mesma coluna à esquerda
        current_btn_y = group_top + estimated_card_height + GAP_CARD_BUTTONS + (BUTTON_HEIGHT / 2)

        btn_defs = [
            ("oppositions", "Filósofos contrários", "#ff6666", (oppositions or {}).get(name, [])),
            ("adepts",      "Filósofos adeptos",    "#66cc66", (adepts     or {}).get(name, [])),
            ("influences",  "Influenciados",         "#6688ff", (influences or {}).get(name, [])),
            ("works",       "Principais obras",      "#aa88cc", (works      or {}).get(name, [])),
        ]

        def est_h(text, chars=28, lh=19, pad=28, min_h=60):
            """Estima a altura de um nó com base no conteúdo textual."""
            lines = sum(1 if p == '' else (len(p) + chars - 1) // chars for p in text.split('\n'))
            return max(min_h, lines * lh + pad)

        # Registro de botões com y e id para linkar nos cards
        button_registry = []

        for i, (btn_key, btn_text, btn_color, btn_items) in enumerate(btn_defs):
            btn_id = f"btn_{safe_name}_{i}"
            btn_node = build_rect_node(
                node_id=btn_id,
                x=left_x, y=current_btn_y,
                width=CARD_WIDTH, height=BUTTON_HEIGHT,
                color=btn_color,
                classes=button_class,
                label=btn_text,
                z_index=11,
                font_size=16
            )
            btn_node["data"]["btn_type"]       = btn_key
            btn_node["data"]["safe_phil_name"] = safe_name
            btn_node["style"]["font-weight"] = "bold"
            elements.append(btn_node)
            button_registry.append((btn_key, btn_color, btn_items, current_btn_y, btn_id))
            current_btn_y += (BUTTON_HEIGHT + GAP_BUTTONS)

        # Cards Laterais: cada card = nó header (negrito) + nó body (texto normal)
        SIDE_X        = CARD_WIDTH + 40
        HEADER_H      = 0
        FONT_SZ       = 14
        GAP_CARD      = 50
        CARD_ANCHOR_Y = group_top
        last_name = name.split()[-1]

        def make_card(header_text, body_text, card_x, ref_y, card_cls, id_prefix, hdr_color, bdr_color):
            """Cria UM nó âncora invisível que carrega o HTML do card (altura automática no CSS).
            ref_y = centro do cabeçalho (mantém a lógica de empilhamento).
            Retorna (nós, id_âncora, altura_estimada)."""
            est_total = HEADER_H + est_h(body_text)
            card_top  = ref_y - HEADER_H / 2
            node_id   = f"{id_prefix}-c"

            anchor = build_rect_node(
                node_id=node_id,
                x=card_x, y=card_top + est_total / 2,
                width=CARD_WIDTH, height=est_total,
                color="rgba(0,0,0,0)",
                classes=card_cls,
                label="",
                border_width=0, z_index=10
            )
            anchor["data"]["html"] = build_side_card_html(header_text, body_text, bdr_color)
            return [anchor], node_id, est_total

        for btn_key, btn_color, btn_items, btn_y, btn_id in button_registry:
            card_cls = f"btn-cards cards-{safe_name} cards-{safe_name}-{btn_key}"

            def place_column(col_items, card_x, col_suffix):
                """Empilha uma lista de (título, desc) a partir de uma posição fixa no topo."""
                heights = [HEADER_H + est_h(d) for _, d in col_items]
                y = CARD_ANCHOR_Y + HEADER_H / 2
                for k, (title, desc) in enumerate(col_items):
                    nodes, anchor_id, _ = make_card(
                        header_text=title, body_text=desc,
                        card_x=card_x, ref_y=y,
                        card_cls=card_cls,
                        id_prefix=f"card-{btn_key}-{safe_name}-{col_suffix}-{k}",
                        hdr_color=btn_color, bdr_color=btn_color
                    )
                    elements.extend(nodes)
                    elements.append({
                        "classes": card_cls,
                        "data": {"id": f"edge-{btn_key}-{safe_name}-{col_suffix}-{k}", "source": btn_id, "target": anchor_id, "lineColor": btn_color}
                    })
                    y += heights[k] + GAP_CARD

            if btn_key == 'works':
                if not btn_items:
                    continue
                if len(btn_items) <= 3:
                    place_column(btn_items, x_pos + SIDE_X, "r")
                else:
                    right_col = [btn_items[j] for j in range(0, len(btn_items), 2)]
                    left_col  = [btn_items[j] for j in range(1, len(btn_items), 2)]
                    place_column(right_col, x_pos + SIDE_X, "r")
                    if left_col:
                        place_column(left_col, x_pos + 2 * SIDE_X, "l")

            elif btn_key == 'influences':
                concordou = [(n, d) for n, d, s in btn_items if s == 'Concorda']
                discordou = [(n, d) for n, d, s in btn_items if s != 'Concorda']
                for group_items, title, x_sign, g_color, g_key in [
                    (concordou, f"{last_name} concordou", 1, "#66cc66", "concordou"),
                    (discordou, f"{last_name} discordou", 2, "#ff6666", "discordou"),
                ]:
                    if not group_items:
                        continue
                    body_text = '\n\n'.join(f"{n}\n{d}" for n, d in group_items)
                    nodes, anchor_id, _ = make_card(
                        header_text=title,
                        body_text=body_text,
                        card_x=x_pos + x_sign * SIDE_X, ref_y=CARD_ANCHOR_Y + HEADER_H / 2,
                        card_cls=card_cls, id_prefix=f"card-inf-{safe_name}-{g_key}",
                        hdr_color=g_color, bdr_color=g_color
                    )
                    elements.extend(nodes)
                    elements.append({
                        "classes": card_cls,
                        "data": {"id": f"edge-inf-{safe_name}-{g_key}", "source": btn_id, "target": anchor_id, "lineColor": btn_color}
                    })

            else:  # oppositions, adepts — centralizados em btn_y
                if btn_items:
                    place_column(btn_items, x_pos + SIDE_X, "r")

    return elements

def build_timeline_elements(data):
    """Função principal de construção da timeline."""

    # Extração de Dados
    epochs        = data.get('epochs', [])
    events        = data.get('events', [])
    philosophies  = data.get('philosophies', {})
    bifurcations  = data.get('bifurcations', [])
    philosophers  = data.get('philosophers', [])
    works         = data.get('works', {})
    influences    = data.get('influences', {})
    adepts        = data.get('adepts', {})
    oppositions   = data.get('oppositions', {})

    # Métricas Base
    events_band_height = data.get('events_band_height', 70)
    min_year, scale_x, total_width, total_height, timeline_center, events_center, philosophy_metrics = general_metrics(philosophies, events_band_height)

    # Config da Faixa de Eventos
    events_band_color          = data.get('events_band_color', '#cc0066')
    events_band_opacity        = data.get('events_band_opacity', 0.08)
    events_band_border_opacity = data.get('events_band_border_opacity', 0.3)
    events_band_staff          = data.get('events_band_staff', False)
    events_band_staff_lines    = data.get('events_band_staff_lines', 5)
    events_band_staff_opacity  = data.get('events_band_staff_opacity', 0.15)
    events_band_staff_color    = data.get('events_band_staff_color')

    # Marcação de Épocas
    epoch_markers = build_epochs(epochs, min_year, scale_x)

    # Construção dos Elementos
    # A faixa entra primeiro na lista: com z-index 0 (empatado com o padrão dos demais nós),
    # o Cytoscape desenha por ordem de inserção, então ela fica atrás de tudo que vier depois.
    elements = []
    elements.extend(build_events_band(
        events_center, events_band_height, events_band_color, events_band_opacity,
        events_band_border_opacity, total_width, events_band_staff,
        events_band_staff_lines, events_band_staff_opacity, events_band_staff_color
    ))
    elements.extend(build_philosophies(philosophy_metrics, bifurcations, min_year, scale_x))
    elements.extend(build_philosophers(philosophers, philosophy_metrics, min_year, scale_x, works, influences, adepts, oppositions))
    elements.extend(build_events(events, min_year, scale_x, events_center))

    return {
        "elements": elements,
        "epochs": epoch_markers,
        "total_width": total_width,
        "total_height": total_height,
        "min_year": min_year,
        "scale_x": scale_x,
        "events_center": events_center,
        "events_band_color": events_band_color,
        "events_band_height": events_band_height,
        "events_band_opacity": events_band_opacity,
        "events_band_border_opacity": events_band_border_opacity,
        "events_band_text_color": data.get("events_band_text_color", "#e0669c"),
        "events_band_font": data.get("events_band_font", "monospace"),
        "events_band_staff": events_band_staff,
        "events_band_staff_lines": events_band_staff_lines,
        "events_band_staff_opacity": events_band_staff_opacity,
        "events_band_staff_color": events_band_staff_color
    }
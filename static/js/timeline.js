import { cyStyles } from '../css/cy_styles.js';

/** Converte cor hex (#rrggbb) em rgba com alpha ajustável. */
function hexToRgba(hex, alpha) {
    const clean = hex.replace('#', '');
    const r = parseInt(clean.substring(0, 2), 16);
    const g = parseInt(clean.substring(2, 4), 16);
    const b = parseInt(clean.substring(4, 6), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

export const TimelineApp = {
    cy: null,
    wrapper: null,

    /** Inicializa a timeline. */
    init(){
        this.wrapper = document.querySelector('#scroll-wrapper');
        this.loadData();
    },

    /** Faz uma chamada para a API da aplicação, retornando os dados já processados para uso. */
    loadData(){
        fetch('/timeline')
            .then(response => {
                if(!response.ok) throw new Error("Erro ao buscar /timeline");
                return response.json();
            })
            .then(data => this.buildGraph(data))
            .catch(error => console.error("Erro no TimelineApp:", error));
    },

    /** Ativa a interatividade dos componentes do grafo. */
    bindInteractivity(){
        // Detecção de Cliques
        this.cy.on('tap', (evt) => {
            const target = evt.target;
            const allUI = '.phil-detail, .clickable-button, .event-detail, .btn-cards';

            // Clique Arbitrário
            if (target === this.cy) {
                this.cy.elements(allUI).style('display', 'none');
                return;
            }

            // Filósofo
            if(target.hasClass('phil-portrait')){
                const philName = target.data('phil_name');
                if(!philName) return;

                const safeName = philName.toLowerCase().replace(/ /g, '_');
                const selector = '.details_' + safeName;
                const details = this.cy.elements(selector);

                const isHidden = details.style('display') === 'none';
                this.cy.elements(allUI).style('display', 'none');

                if(isHidden && details.length > 0){
                    details.style('display', 'element');
                }
                return;
            }

            // Evento
            if (target.hasClass('event')) {
                const eventId = target.data('event_id');
                if (!eventId) return;

                const selector = '.details_' + eventId;
                const details = this.cy.elements(selector);
                const isHidden = details.style('display') === 'none';

                this.cy.elements(allUI).style('display', 'none');

                if (isHidden && details.length > 0) {
                    details.style('display', 'element');
                }
                return;
            }

            // Coisas não interativas mas que não devem desativar nada
            if(target.hasClass('phil-detail', 'event-detail')){
                return;
            }

            // Botões de ação do filósofo
            if(target.hasClass('clickable-button')){
                const safeName = target.data('safe_phil_name');
                const btnKey   = target.data('btn_type');

                const allPhilCards = this.cy.elements(`.cards-${safeName}`);
                const thisGroup    = this.cy.elements(`.cards-${safeName}-${btnKey}`);
                const isHidden     = thisGroup.length === 0 || thisGroup.first().style('display') === 'none';

                allPhilCards.style('display', 'none');
                if(isHidden && thisGroup.length > 0){
                    thisGroup.style('display', 'element');
                }
                return;
            }

            this.cy.elements(allUI).style('display', 'none');
        });
    },

    /** Cria o grafo que representa a timeline. Qualquer abstração de qualquer tipo de grafo interage com esse grafo geral criado. */
    buildGraph(data){
        // Escala de elementos


        // Plotagem da épocas no fundo
        if(data.epochs){
            data.epochs.forEach(ep => {
                const line = document.createElement('div');
                line.className = 'epoch-line';
                line.style.left = `${ep.x_pos}px`;
                line.style.height = `${data.total_height}px`;

                const label = document.createElement('div');
                label.className = 'epoch-label';
                label.style.left = `${ep.x_pos}px`;
                label.innerText = ep.label;

                this.wrapper.appendChild(line);
                this.wrapper.appendChild(label);
            });
        }

        // Faixa indicando a região dos eventos históricos
        if(typeof data.events_center === 'number'){
            const bandColor  = data.events_band_color      || '#cc0066';
            const bandHeight = data.events_band_height      || 70;
            const bandOpacity = data.events_band_opacity !== undefined ? data.events_band_opacity : 0.08;
            const bandBorderOpacity = data.events_band_border_opacity !== undefined ? data.events_band_border_opacity : 0.3;
            const textColor  = data.events_band_text_color  || bandColor;
            const textFont   = data.events_band_font        || 'monospace';
            // Mesma unidade de coordenadas usada pelos eventos (y_pos = events_center + y_offset,
            // sem nenhuma escala extra) - o container do cytoscape já é dimensionado 1:1 em px.
            const bandY = data.events_center;
 
            // Faixa preenchida, levemente transparente, sem interceptar cliques
            const band = document.createElement('div');
            band.className = 'events-band';
            band.style.top = `${bandY - bandHeight / 2}px`;
            band.style.height = `${bandHeight}px`;
            band.style.width = `${data.total_width}px`;
            band.style.backgroundColor = hexToRgba(bandColor, bandOpacity);
            band.style.borderTop = `1px solid ${hexToRgba(bandColor, bandBorderOpacity)}`;
            band.style.borderBottom = `1px solid ${hexToRgba(bandColor, bandBorderOpacity)}`;
 
            // Rótulo: acompanha o scroll junto com o resto do conteúdo (posição absoluta,
            // centralizado horizontalmente ao longo de toda a largura da timeline)
            const label = document.createElement('div');
            label.className = 'events-band-label';
            label.style.top = `${bandY}px`;
            label.style.left = `${data.total_width / 2}px`;
            label.style.setProperty('--events-band-label-color', hexToRgba(textColor, 0.6));
            label.style.setProperty('--events-band-label-font', textFont);
            label.innerText = 'Eventos Históricos e Científicos Importantes';
 
            this.wrapper.appendChild(band);
            this.wrapper.appendChild(label);
 
            // Aspecto de partitura (opcional): linhas horizontais suaves dentro da faixa
            if(data.events_band_staff){
                const staffLines = data.events_band_staff_lines || 5;
                const staffOpacity = data.events_band_staff_opacity !== undefined ? data.events_band_staff_opacity : 0.15;
                const staffColor = data.events_band_staff_color || bandColor;
                const spacing = bandHeight / (staffLines + 1);
 
                for(let i = 1; i <= staffLines; i++){
                    const staffLine = document.createElement('div');
                    staffLine.className = 'events-band-staff-line';
                    staffLine.style.top = `${bandY - bandHeight / 2 + spacing * i}px`;
                    staffLine.style.width = `${data.total_width}px`;
                    staffLine.style.backgroundColor = hexToRgba(staffColor, staffOpacity);
                    this.wrapper.appendChild(staffLine);
                }
            }
        }

        // Criação do grafo com passagem dos elementos já processados
        const cyContainer = document.createElement('div');
        cyContainer.id = 'cy';
        cyContainer.style.width = `${data.total_width}px`;
        cyContainer.style.height = `${data.total_height}px`;
        this.wrapper.appendChild(cyContainer);

        cytoscape.warnings(false);
        this.cy = cytoscape({
            container: cyContainer,
            elements: data.elements,
            zoomingEnabled: false,
            panningEnabled: false,
            boxSelectionEnabled: false,
            autoungrabify: true,
            autounselectify: true,
            style: cyStyles,
            layout: { name: 'preset' }
        });

        // Ativa Interatividade
        this.bindInteractivity();

        // Cards HTML em tópicos sobre os nós de resumo
        this.setupHtmlCards();
    },

    /** Cria as divs HTML dos cards de resumo e as ancora sobre os nós correspondentes. */
    setupHtmlCards(){
        const overlay = document.createElement('div');
        overlay.className = 'html-card-overlay';
        this.cy.container().appendChild(overlay);

        this.htmlCards = {};
        this.cy.nodes().forEach(node => {
            const html = node.data('html');
            if(!html) return;

            const div = document.createElement('div');
            div.className = 'html-card-wrapper';
            div.innerHTML = html;

            const pos = node.renderedPosition();
            div.style.left = `${pos.x}px`;
            div.style.top  = `${pos.y}px`;
            div.style.display = node.style('display') === 'none' ? 'none' : 'block';

            overlay.appendChild(div);
            this.htmlCards[node.id()] = div;
        });

        // Após cada clique, espelha a visibilidade dos cards HTML na dos nós.
        this.cy.on('tap', () => this.refreshHtmlCards());
    },

    /** Sincroniza a visibilidade das divs HTML com o estado de exibição dos nós. */
    refreshHtmlCards(){
        if(!this.htmlCards) return;
        Object.keys(this.htmlCards).forEach(id => {
            const node = this.cy.getElementById(id);
            this.htmlCards[id].style.display = node.style('display') === 'none' ? 'none' : 'block';
        });
    }
};
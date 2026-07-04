import { cyStyles } from '../css/cy_styles.js';

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

    init(){
        this.wrapper = document.querySelector('#scroll-wrapper');
        this.loadData();
    },

    loadData(){
        fetch('/timeline')
            .then(response => {
                if(!response.ok) throw new Error("Erro ao buscar /timeline");
                return response.json();
            })
            .then(data => this.buildGraph(data))
            .catch(error => console.error("Erro no TimelineApp:", error));
    },

    bindInteractivity(){
        // Detecção de Cliques
        this.cy.on('tap', (evt) => {
            const target = evt.target;
            const allUI = '.phil-detail, .clickable-button, .event-detail, .btn-cards';

            if (target === this.cy) {
                this.cy.elements(allUI).style('display', 'none');
                return;
            }

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

            if(target.hasClass('phil-detail', 'event-detail')){
                return;
            }

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

    buildGraph(data){
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

        if(typeof data.events_center === 'number'){
            const bandColor = data.events_band_color || '#cc0066';
            const textColor = data.events_band_text_color || bandColor;
            const textFont  = data.events_band_font || 'monospace';
            const bandY = data.events_center;

            const label = document.createElement('div');
            label.className = 'events-band-label';
            label.style.top = `${bandY}px`;
            label.style.left = `${data.total_width / 2}px`;
            label.style.setProperty('--events-band-label-color', hexToRgba(textColor, 0.6));
            label.style.setProperty('--events-band-label-font', textFont);
            label.innerText = 'Eventos Históricos e Científicos Importantes';

            this.wrapper.appendChild(label);
        }

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

        this.bindInteractivity();
        this.setupHtmlCards();
    },

    setupHtmlCards(){
        const overlay = document.createElement('div');
        overlay.className = 'html-card-overlay';
        this.cy.container().appendChild(overlay);

        this.htmlCards = {};
        this.cy.nodes().forEach(node => {
            const html = node.data('html');
            if(!html) return;

            const div = document.createElement('div');
            div.className = 'html-card-wrapper ' + node.classes().join(' ');
            div.innerHTML = html;

            const pos = node.renderedPosition();
            div.style.left = `${pos.x}px`;
            div.style.top  = `${pos.y}px`;
            div.style.display = node.style('display') === 'none' ? 'none' : 'block';

            overlay.appendChild(div);
            this.htmlCards[node.id()] = div;
        });
        this.cy.on('tap', () => this.refreshHtmlCards());
    },

    refreshHtmlCards(){
        if(!this.htmlCards) return;
        Object.keys(this.htmlCards).forEach(id => {
            const node = this.cy.getElementById(id);
            this.htmlCards[id].style.display = node.style('display') === 'none' ? 'none' : 'block';
        });
    }
};
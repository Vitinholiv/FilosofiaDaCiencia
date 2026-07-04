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
    sizerEl: null,
    contentEl: null,
    zoomLevel: null,
    minZoom: 0.2,
    baseWidth: 0,
    baseHeight: 0,

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
        this.baseWidth  = data.total_width;
        this.baseHeight = data.total_height;

        this.sizerEl = document.createElement('div');
        this.sizerEl.id = 'zoom-sizer';
        this.sizerEl.style.position = 'relative';
        this.wrapper.appendChild(this.sizerEl);

        this.contentEl = document.createElement('div');
        this.contentEl.id = 'zoom-content';
        this.contentEl.style.position = 'absolute';
        this.contentEl.style.top = '0';
        this.contentEl.style.left = '0';
        this.contentEl.style.width  = `${data.total_width}px`;
        this.contentEl.style.height = `${data.total_height}px`;
        this.contentEl.style.transformOrigin = '0 0';
        this.sizerEl.appendChild(this.contentEl);

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

                this.contentEl.appendChild(line);
                this.contentEl.appendChild(label);
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

            this.contentEl.appendChild(label);
        }

        const cyContainer = document.createElement('div');
        cyContainer.id = 'cy';
        cyContainer.style.width = `${data.total_width}px`;
        cyContainer.style.height = `${data.total_height}px`;
        this.contentEl.appendChild(cyContainer);

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

        this.minZoom = window.innerHeight / this.baseHeight;
        this.setZoom(Math.max(1, this.minZoom));

        window.addEventListener('resize', () => {
            this.minZoom = window.innerHeight / this.baseHeight;
            this.fitHeightIfNeeded();
        });
    },

    setZoom(zoom, anchorClientX, anchorClientY){
        const oldZoom = this.zoomLevel;
        const newZoom = Math.max(this.minZoom, Math.min(3, zoom));
        if(oldZoom !== null && newZoom === oldZoom) return;

        const wrapper = this.wrapper;
        let scrollLeft = wrapper.scrollLeft;
        let scrollTop  = wrapper.scrollTop;

        if(oldZoom !== null && anchorClientX !== undefined && anchorClientY !== undefined){
            const rect = wrapper.getBoundingClientRect();
            const cursorX = anchorClientX - rect.left;
            const cursorY = anchorClientY - rect.top;

            const baseX = (scrollLeft + cursorX) / oldZoom;
            const baseY = (scrollTop  + cursorY) / oldZoom;

            scrollLeft = baseX * newZoom - cursorX;
            scrollTop  = baseY * newZoom - cursorY;
        }

        this.zoomLevel = newZoom;
        this.contentEl.style.transform = `scale(${this.zoomLevel})`;
        this.sizerEl.style.width  = `${this.baseWidth  * this.zoomLevel}px`;
        this.sizerEl.style.height = `${this.baseHeight * this.zoomLevel}px`;

        wrapper.scrollLeft = scrollLeft;
        wrapper.scrollTop  = scrollTop;

        if(this.cy){
            this.cy.resize();
        }
    },

    fitHeightIfNeeded(){
        if(this.zoomLevel < this.minZoom){
            this.setZoom(this.minZoom);
        }
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
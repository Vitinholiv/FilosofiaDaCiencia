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
    zoomLevel: 1,
    minZoom: 0.1,
    baseWidth: 0,
    baseHeight: 0,

    init(){
        this.wrapper = document.querySelector('#scroll-wrapper');
        return this.loadData();
    },

    loadData(){
        return fetch('/timeline')
            .then(response => {
                if(!response.ok) throw new Error("Erro ao buscar /timeline");
                return response.json();
            })
            .then(data => this.buildGraph(data))
            .catch(error => console.error("Erro no TimelineApp:", error));
    },

    extractSafeName(classesStr){
        if(!classesStr) return null;
        const tokens = classesStr.split(/\s+/);
        const token = tokens.find(t => t.indexOf('details_') === 0);
        return token ? token.slice('details_'.length) : null;
    },

    measureCardHeights(elements){
        const container = document.createElement('div');
        container.className = 'html-card-wrapper';
        container.style.position = 'absolute';
        container.style.left = '-99999px';
        container.style.top = '0';
        container.style.visibility = 'hidden';
        document.body.appendChild(container);

        const groups = {};
        elements.forEach(el => {
            const safeName = this.extractSafeName(el.classes);
            if(!safeName) return;

            if(el.classes.includes('phil-detail') && el.data && el.data.html){
                (groups[safeName] = groups[safeName] || {}).summary = el;
            } else if(el.classes.includes('clickable-button')){
                const g = (groups[safeName] = groups[safeName] || {});
                (g.buttons = g.buttons || []).push(el);
            }
        });

        Object.values(groups).forEach(group => {
            if(!group.summary || !group.buttons || !group.buttons.length) return;

            const estimatedHeight = group.summary.style && group.summary.style.height;
            if(typeof estimatedHeight !== 'number') return;

            container.innerHTML = group.summary.data.html;
            const actualHeight = container.getBoundingClientRect().height;
            const delta = actualHeight - estimatedHeight;

            if(Math.abs(delta) < 0.5) return;
            group.summary.position.y += delta / 2;
            group.summary.style.height = actualHeight;

            group.buttons.forEach(btn => { btn.position.y += delta; });
        });

        document.body.removeChild(container);
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

        this.measureCardHeights(data.elements);

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

        this.cy.on('mouseover', 'node.phil-portrait, node.event', (evt) => {
            evt.target.animate({ style: { 'border-width': 4 } }, { duration: 100 });
        });
        this.cy.on('mouseout', 'node.phil-portrait, node.event', (evt) => {
            evt.target.animate({ style: { 'border-width': 3 } }, { duration: 100 });
        });

        this.setupHtmlCards();

        // Zoom inicial: sempre exatamente 100% (zoom real = 1), aplicado na
        // hora, sem animação e sem depender de um cálculo assíncrono de
        // minZoom (era isso que fazia o zoom inicial "vazar" para um valor
        // maior que 1 em telas mais altas).
        this.minZoom = this.computeMinZoom();
        this.targetZoom = 1;
        this._applyZoom(1, null);

        window.addEventListener('resize', () => {
            this.minZoom = this.computeMinZoom();
            if(this.targetZoom < this.minZoom){
                this.setZoom(this.minZoom);
            }
        });
    },

    computeMinZoom(){
        // Impede dar zoom out a ponto de sobrar espaço vazio abaixo/acima do
        // conteúdo, mas o teto é 1: nunca força um zoom inicial (ou mínimo)
        // maior que 100%. Isso é o que antes causava o zoom "estranho" ao
        // carregar a página em telas com altura maior que o conteúdo.
        const fitZoom = window.innerHeight / this.baseHeight;
        return Math.min(1, Math.max(0.1, fitZoom));
    },

    targetZoom: 1,
    zoomAnimId: null,
    setZoom(zoom, anchorClientX, anchorClientY){
        this.targetZoom = Math.max(this.minZoom, Math.min(3, zoom));
        this._zoomAnchor = (anchorClientX !== undefined) ? { x: anchorClientX, y: anchorClientY } : null;
        if(!this.zoomAnimId){
            this.zoomAnimId = requestAnimationFrame(() => this._stepZoom());
        }
    },

    _stepZoom(){
        const oldZoom = this.zoomLevel;
        const diff = this.targetZoom - oldZoom;
        if(Math.abs(diff) < 0.001){
            this._applyZoom(this.targetZoom, this._zoomAnchor);
            this.zoomAnimId = null;
            return;
        }
        const newZoom = oldZoom + diff * 0.65; 
        this._applyZoom(newZoom, this._zoomAnchor);
        this.zoomAnimId = requestAnimationFrame(() => this._stepZoom());
    },

    _applyZoom(newZoom, anchor){
        const oldZoom = this.zoomLevel;

        const wrapper = this.wrapper;
        let scrollLeft = wrapper.scrollLeft;
        let scrollTop  = wrapper.scrollTop;

        if(anchor){
            const rect = wrapper.getBoundingClientRect();
            const cursorX = anchor.x - rect.left;
            const cursorY = anchor.y - rect.top;

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
            div.style.display = 'none';

            const pos = node.renderedPosition();
            div.style.left = `${pos.x}px`;
            div.style.top  = `${pos.y}px`;

            overlay.appendChild(div);
            this.htmlCards[node.id()] = div;
        });
        this.cy.on('tap', () => this.refreshHtmlCards());
    },

    refreshHtmlCards(){
        if(!this.htmlCards) return;

        const toShow = [];
        Object.keys(this.htmlCards).forEach(id => {
            const node = this.cy.getElementById(id);
            const el = this.htmlCards[id];
            const shouldShow = node.style('display') !== 'none';

            if(shouldShow){
                if(el.style.display === 'none'){
                    el.style.display = 'block';
                    el.classList.remove('card-visible');
                    void el.offsetWidth;
                }
                toShow.push(el);
            } else if(el.classList.contains('card-visible')){
                el.classList.remove('card-visible');
                setTimeout(() => {
                    if(!el.classList.contains('card-visible')) el.style.display = 'none';
                }, 200);
            } else {
                el.style.display = 'none';
            }
        });

        toShow.forEach((el, i) => {
            setTimeout(() => el.classList.add('card-visible'), i * 60);
        });
    }
};
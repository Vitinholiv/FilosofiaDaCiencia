export const TimelineApp = {
    cy: null,
    wrapper: null,
    tooltip: null,
    activeNode: null,
    isOverTooltip: false,

    init() {
        this.wrapper = document.querySelector('#scroll-wrapper');
        this.setupTooltipDOM();
        this.loadData();
    },

    setupTooltipDOM() {
        this.tooltip = document.getElementById('custom-tooltip');
        if (!this.tooltip) {
            this.tooltip = document.createElement('div');
            this.tooltip.id = 'custom-tooltip';
            document.body.appendChild(this.tooltip);
        }
    },

    loadData() {
        fetch('/timeline')
            .then(response => {
                if (!response.ok) throw new Error("Erro ao buscar /timeline");
                return response.json();
            })
            .then(data => this.buildGraph(data))
            .catch(error => console.error("Erro no TimelineApp:", error));
    },

    buildGraph(data) {
        const cyContainer = document.createElement('div');
        cyContainer.id = 'cy';
        cyContainer.style.width = `${data.total_width}px`;
        cyContainer.style.height = `${data.total_height}px`;
        
        this.wrapper.appendChild(cyContainer);

        this.cy = cytoscape({
            container: cyContainer,
            elements: data.elements,
            zoomingEnabled: false,
            panningEnabled: false,
            boxSelectionEnabled: false,
            autoungrabify: true,
            autounselectify: true,
            style: this.getStyles(),
            layout: { name: 'preset' }
        });

        this.bindEvents();
    },

    getStyles() {
        return [
            {
                selector: 'node',
                style: {
                    'shape': 'round-rectangle',
                    'width': 'data(width)',
                    'height': 'data(height)',
                    'background-color': 'rgba(138, 180, 248, 0.05)',
                    'border-width': 1,
                    'border-color': 'rgba(138, 180, 248, 0.4)',
                    'label': 'data(id)',
                    'color': '#8ab4f8',
                    'font-size': '16px',
                    'text-margin-y': '10px',
                    'text-valign': 'bottom',
                    'text-halign': 'center',
                    'font-family': 'monospace',
                    'text-color': '#000000'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 4,
                    'line-color': 'data(targetColor)',
                    'target-arrow-color': 'data(targetColor)',
                    'target-arrow-shape': 'none',
                    'curve-style': 'bezier',
                    'edge-distances': 'node-position'
                }
            },
            {
                selector: 'node.bottom-event',
                style: { 'label': '', 'shape': 'ellipse', 'width': 20, 'height': 20, 'border-width': 1 }
            },
            {
                selector: 'node.bottom-event.hover',
                style: { 'width': 26, 'height': 26, 'border-width': 2 }
            },
            {
                selector: '.phil-detail',
                style: { 'display': 'none' }
            }
        ];
    },

    bindEvents() {
        const self = this; 

        this.cy.on('mouseover', 'node.bottom-event', function(evt) {
            const node = evt.target;
            const text = node.data('tooltip');
            
            self.activeNode = node; 
            node.addClass('hover');
            if (!text) return;

            const imgUrls = node.data('imgUrls') || []; 
            let content = '';
            
            if (imgUrls.length > 0) {
                imgUrls.forEach(url => {
                    content += `<img src="${url}" style="width:100%;max-height:140px;object-fit:cover;border-radius:3px;margin-bottom:8px;display:block;">`;
                });
            }
            content += `<span>${text}</span>`;

            self.tooltip.innerHTML = content;
            self.tooltip.style.display = 'block';

            if (self.tooltip.querySelector('a')) {
                self.tooltip.classList.add('has-links');
                self.tooltip.querySelectorAll('a').forEach(a => {
                    a.style.color = '#0066cc';
                    a.style.wordBreak = 'break-word';
                    a.target = '_blank'; 
                    a.rel = 'noopener';
                });
            } else {
                self.tooltip.classList.remove('has-links');
            }

            const pos = node.renderedPosition();
            const rect = self.cy.container().getBoundingClientRect();
            self.tooltip.style.left = `${rect.left + pos.x - self.tooltip.offsetWidth / 2}px`;
            self.tooltip.style.top  = `${rect.top  + pos.y - self.tooltip.offsetHeight - 15}px`;
        });

        this.cy.on('mouseout', 'node.bottom-event', function() {
            setTimeout(() => {
                if (!self.isOverTooltip) self.hideTooltip();
            }, 80);
        });

        this.tooltip.addEventListener('mouseenter', () => self.isOverTooltip = true);
        this.tooltip.addEventListener('mouseleave', () => {
            self.isOverTooltip = false;
            self.hideTooltip();
        });

        this.wrapper.addEventListener('scroll', () => {
            self.hideTooltip();
            self.cy.nodes('.bottom-event.hover').removeClass('hover');
        });

        this.cy.on('tap', function(evt) {
            if (evt.target === self.cy) self.hideTooltip();
        });

        this.cy.on('tap', 'node.phil-portrait', function(evt) {
            const node = evt.target;
            const philName = node.data('phil_name');
            
            if (!philName) return; 

            const selector = '.details_' + philName.replace(/ /g, '_');
            const details  = self.cy.elements(selector);

            if (details.length > 0) {
                const isHidden = details.style('display') === 'none';
                details.style('display', isHidden ? 'element' : 'none');
            }
        });
    },

    hideTooltip() {
        this.tooltip.style.display = 'none';
        if (this.activeNode) {
            this.activeNode.removeClass('hover');
            this.activeNode = null;
        }
    }
};
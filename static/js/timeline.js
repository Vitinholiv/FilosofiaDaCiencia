import { cyStyles } from '../css/cy_styles.js';
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
        const realHeightPx = window.innerHeight;
        const scaleY = realHeightPx / data.total_height;

        // Escala de elementos
        data.elements.forEach(el => {
            if(el.position && el.position.y){
                el.position.y = el.position.y * scaleY;
            }
        });

        // Plotagem da épocas no fundo
        if(data.epochs){
            data.epochs.forEach(ep => {
                const line = document.createElement('div');
                line.className = 'epoch-line';
                line.style.left = `${ep.x_pos}px`;

                const label = document.createElement('div');
                label.className = 'epoch-label';
                label.style.left = `${ep.x_pos}px`;
                label.innerText = ep.label;

                this.wrapper.appendChild(line);
                this.wrapper.appendChild(label);
            });
        }

        // Criação do grafo com passagem dos elementos já processados
        const cyContainer = document.createElement('div');
        cyContainer.id = 'cy';
        cyContainer.style.width = `${data.total_width}px`;
        cyContainer.style.height = `100vh`;
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
    }
};
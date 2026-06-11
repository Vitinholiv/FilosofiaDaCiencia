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
                if (!response.ok) throw new Error("Erro ao buscar /timeline");
                return response.json();
            })
            .then(data => this.buildGraph(data))
            .catch(error => console.error("Erro no TimelineApp:", error));
    },

    /** Cria o grafo que representa a timeline. Qualquer abstração de qualquer tipo de grafo interage com esse grafo geral criado. */
    buildGraph(data){
        const realHeightPx = window.innerHeight;
        const scaleY = realHeightPx / data.total_height;

        // Escala de elementos
        data.elements.forEach(el => {
            if (el.position && el.position.y){
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
    }
};
var rawData = document.getElementById('elements-data').textContent;
var elements = JSON.parse(rawData);

var cy = cytoscape({
    container: document.getElementById('cy'),
    elements: elements,
    zoomingEnabled: false,
    panningEnabled: false,
    boxSelectionEnabled: false,
    autoungrabify: true,
    autounselectify: true,

    style: [
        {
            selector: 'node',
            style: {
                'shape': 'round-rectangle',
                'width': 'data(width)',
                'height': 3,
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
        {   // Style dos eventos históricos/trabalhos
            selector: 'node.bottom-event',
            style: {
                'label': '',
                'shape': 'ellipse',
                'width': 20,
                'height': 20,
                'border-width': 1
            }
        },
        {   // Style para o zoom
            selector: 'node.bottom-event.hover',
            style: {
                'width': 26,
                'height': 26,
                'border-width': 2
            }
        },
        {
            selector: '.phil-detail',
            style: {
                'display': 'none'
            }
        }
    ],
    layout: {
        name: 'preset' 
    }
});

// Cria o elemento HTML do tooltip
var tooltip = document.createElement('div');
tooltip.id = 'custom-tooltip';
document.body.appendChild(tooltip);

// Quando o mouse passar por cima da bolinha
cy.on('mouseover', 'node.bottom-event', function(evt){
    var node = evt.target;
    var text = node.data('tooltip');

    node.addClass('hover');

    if (!text) return;

    tooltip.innerHTML = text;
    tooltip.style.display = 'block';

    var pos = node.renderedPosition();
    var cyContainer = cy.container().getBoundingClientRect();
    
    // Centraliza o balão e posiciona acima do nó
    var leftPos = cyContainer.left + pos.x - (tooltip.offsetWidth / 2);
    var topPos = cyContainer.top + pos.y - tooltip.offsetHeight - 15;

    tooltip.style.left = leftPos + 'px';
    tooltip.style.top = topPos + 'px';
});

// Quando o mouse sair da bolinha
cy.on('mouseout', 'node.bottom-event', function(evt){
    evt.target.removeClass('hover'); 
    tooltip.style.display = 'none';
});


// Alternar visibilidade ao clicar na foto do filósofo
cy.on('tap', 'node.phil-portrait', function(evt){
    var node = evt.target;
    var philName = node.data('phil_name');
    
    var detailSelector = '.details_' + philName.replace(/ /g, '_');
    var detailsElements = cy.elements(detailSelector);
    
    if (detailsElements.length > 0) {
        // Se o estilo computado atual for 'none', muda para 'element' (visível), senão esconde
        if (detailsElements.style('display') === 'none') {
            detailsElements.style('display', 'element');
        } else {
            detailsElements.style('display', 'none');
        }
    }
});

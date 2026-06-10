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
        {
            selector: 'node.bottom-event',
            style: {
                'label': '',
                'shape': 'ellipse',
                'width': 20,
                'height': 20,
                'border-width': 1
            }
        },
        {
            selector: 'node.bottom-event.hover',
            style: { 'width': 26, 'height': 26, 'border-width': 2 }
        },
        {
            // Todos os detalhes ficam ocultos por padrão
            selector: '.phil-detail',
            style: { 'display': 'none' }
        }
    ],
    layout: { name: 'preset' }
});

// ─── Tooltip para bottom-events ────────────────────────────────────────────
var tooltip = document.createElement('div');
tooltip.id = 'custom-tooltip';
document.body.appendChild(tooltip);

// Variáveis de controle de hover
var activeNode = null;
var isOverTooltip = false;

// Quando o mouse passar por cima da bolinha
cy.on('mouseover', 'node.bottom-event', function(evt) {
    var node = evt.target;
    var text = node.data('tooltip');
    
    activeNode = node; 
    node.addClass('hover');
    if (!text) return;

    var imgUrls = node.data('imgUrls') || []; 
    
    // Monta o conteúdo do balão com imagem opcional
    var content = '';
    if (imgUrls.length > 0) {
        imgUrls.forEach(function(url) {
            content += '<img src="' + url + '" style="width:100%;max-height:140px;object-fit:cover;border-radius:3px;margin-bottom:8px;display:block;">';
        });
    }
    content += '<span>' + text + '</span>';

    tooltip.innerHTML = content;
    tooltip.style.display = 'block';

    // Ativa pointer-events se houver links clicáveis
    if (tooltip.querySelector('a')) {
        tooltip.classList.add('has-links');
    } else {
        tooltip.classList.remove('has-links');
    }

    tooltip.querySelectorAll('a').forEach(function(a) {
        a.style.color = '#0066cc';
        a.style.wordBreak = 'break-word';
        a.target = '_blank'; 
        a.rel = 'noopener';
    });

    var pos = node.renderedPosition();
    var rect = cy.container().getBoundingClientRect();
    tooltip.style.left = (rect.left + pos.x - tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top  = (rect.top  + pos.y - tooltip.offsetHeight - 15) + 'px';
});

// Quando o mouse sair da bolinha
cy.on('mouseout', 'node.bottom-event', function(evt){
    setTimeout(function() {
        if (!isOverTooltip) {
            tooltip.style.display = 'none';
            if (activeNode) {
                activeNode.removeClass('hover');
                activeNode = null;
            }
        }
    }, 80);
});

tooltip.addEventListener('mouseenter', function() {
    isOverTooltip = true;
});

tooltip.addEventListener('mouseleave', function() {
    isOverTooltip = false;
    tooltip.style.display = 'none';
    if (activeNode) {
        activeNode.removeClass('hover');
        activeNode = null;
    }
});

// Esconde o tooltip após scroll 
document.querySelector('.scroll-wrapper').addEventListener('scroll', function(){
    tooltip.style.display = 'none';
    // Removemos a classe hover de todos os nós caso algum fique travado
    cy.nodes('.bottom-event.hover').removeClass('hover');
});

// ─── Clique no retrato: mostra/oculta TODOS os detalhes do filósofo ────────
cy.on('tap', 'node.phil-portrait', function(evt) {
    var node     = evt.target;
    var philName = node.data('phil_name');
    
    // Evita erro caso você clique em um nó que não possua a propriedade phil_name
    if (!philName) return; 

    var selector = '.details_' + philName.replace(/ /g, '_');
    var details  = cy.elements(selector);

    if (details.length > 0) {
        var isHidden = details.style('display') === 'none';
        details.style('display', isHidden ? 'element' : 'none');
    }
});

// ─── Fechar tooltip ao clicar no fundo ─────────────────────────────────────
cy.on('tap', function(evt) {
    if (evt.target === cy) {
        tooltip.style.display = 'none';
    }
});
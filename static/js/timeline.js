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
                'height': 5,
                'background-color': 'rgba(138, 180, 248, 0.05)',
                'border-width': 1,
                'border-color': 'rgba(138, 180, 248, 0.4)',
                'label': 'data(id)',
                'color': '#8ab4f8', 
                'font-size': '25px',
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
                'width': 5,
                'line-color': 'data(targetColor)',
                'target-arrow-color': 'data(targetColor)',
                'target-arrow-shape': 'none',
                'curve-style': 'taxi', 
                'taxi-direction': 'rightward',
                'taxi-radius': 90, 
                'edge-distances': 'node-position'
            }
        }
    ],
    layout: {
        name: 'preset' 
    }
});
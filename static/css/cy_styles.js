/** Estilos do cytoscape */
export const cyStyles = [
    {
        selector: 'node.philosophy',
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
        selector: 'edge.philosophy',
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
        selector: 'node.event',
        style: { 'label': '', 'shape': 'ellipse', 'width': 20, 'height': 20, 'border-width': 1 }
    },
    {
        selector: 'node.event.hover',
        style: { 'width': 26, 'height': 26, 'border-width': 2 }
    },
    {
        selector: '.phil-detail',
        style: { 'display': 'none' }
    }
];
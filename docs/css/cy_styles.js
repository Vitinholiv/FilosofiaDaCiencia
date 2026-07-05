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
            'font-family': 'monospace'
        }
    },
    {
        selector: 'node[img]',
        style: {
            'background-image': 'data(img)',
            'background-fit': 'cover',
            'background-color': '#ffffff'
        }
    },
    {
        selector: '.circle-node',
        style: {
            'shape': 'ellipse',
            'z-index': 8,
            'label': 'data(label)',
            'text-valign': 'bottom',
            'text-margin-y': 8,
            'font-size': 11,
            'font-weight': 'bold',
            'color': '#ccc',
            'text-wrap': 'wrap'
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
        selector: '.rect-node',
        style: {
            'shape': 'round-rectangle',
            'label': 'data(label)',
            'text-valign': 'center',
            'text-halign': 'center',
            'text-wrap': 'wrap',
            'font-size': 11,
            'color': '#000',
            'border-color': '#888'
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
        selector: '.phil-detail, .event-detail',
        style: { 'display': 'none' }
    },
    {
        selector: '.clickable-button',
        style: { 'display': 'none' }
    },
    {
        selector: '.btn-cards',
        style: { 'display': 'none' }
    },
    {
        selector: 'node.card-header',
        style: { 'font-weight': 'bold', 'text-valign': 'center' }
    },
    {
        selector: 'edge.btn-cards',
        style: {
            'width': 2,
            'line-color': 'data(lineColor)',
            'target-arrow-shape': 'none',
            'curve-style': 'bezier'
        }
    },
    {
        selector: '.dashed-link',
        style: {
            'width': 2,
            'line-color': '#b3b3b3',
            'line-style': 'dashed',
            'target-arrow-shape': 'none',
            'curve-style': 'straight'
        }
    },
];
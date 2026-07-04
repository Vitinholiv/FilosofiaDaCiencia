import { setup_scroll } from './scroller.js';
import { TimelineApp } from './timeline.js';

document.addEventListener('DOMContentLoaded', function() {
    const loading = document.createElement('div');
    loading.id = 'loading-indicator';
    loading.innerText = 'Carregando linha do tempo...';
    document.body.appendChild(loading);

    setup_scroll();
    TimelineApp.init().then(() => {
        loading.classList.add('hidden');
        setTimeout(() => loading.remove(), 300);
    });
});
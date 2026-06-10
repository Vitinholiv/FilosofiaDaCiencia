import { setup_scroll } from './scroller.js';
import { TimelineApp } from './timeline.js';

document.addEventListener('DOMContentLoaded', function() {
    // Prepara o Wrapper da Visualização
    setup_scroll();

    // Linha do Tempo
    TimelineApp.init();
});
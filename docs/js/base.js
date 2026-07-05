import { setup_scroll } from './scroller.js';
import { TimelineApp } from './timeline.js';

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js').catch(err => console.warn('SW falhou:', err));
    });
}

document.addEventListener('DOMContentLoaded', function() {
    setup_scroll();
    TimelineApp.init();
});
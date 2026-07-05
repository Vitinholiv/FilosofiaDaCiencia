import { TimelineApp } from './timeline.js';

export function setup_scroll() {
    const scrollWrapper = document.querySelector('#scroll-wrapper');

    scrollWrapper.addEventListener('wheel', function(event) {
        event.preventDefault();
        const factor = event.deltaY < 0 ? 1.1 : 1 / 1.1;
        TimelineApp.setZoom(TimelineApp.zoomLevel * factor, event.clientX, event.clientY);
    }, { passive: false });

    // Clicar-e-arrastar: inalterado
    let dragging = false;
    let startX = 0, startY = 0, startLeft = 0, startTop = 0;

    scrollWrapper.style.cursor = 'grab';

    scrollWrapper.addEventListener('mousedown', function(event) {
        if (event.button !== 0) return;
        dragging = true;
        startX = event.clientX;
        startY = event.clientY;
        startLeft = scrollWrapper.scrollLeft;
        startTop = scrollWrapper.scrollTop;
        scrollWrapper.style.cursor = 'grabbing';
    }, true);

    window.addEventListener('mousemove', function(event) {
        if (!dragging) return;
        event.preventDefault();
        scrollWrapper.scrollLeft = startLeft - (event.clientX - startX);
        scrollWrapper.scrollTop  = startTop  - (event.clientY - startY);
    });

    window.addEventListener('mouseup', function() {
        if (!dragging) return;
        dragging = false;
        scrollWrapper.style.cursor = 'grab';
    });
}

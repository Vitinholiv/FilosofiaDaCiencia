export function setup_scroll() {
    const scrollWrapper = document.querySelector('#scroll-wrapper');
    scrollWrapper.addEventListener('wheel', function(event) {
        if (event.deltaY !== 0) {
            event.preventDefault();
            scrollWrapper.scrollLeft += event.deltaY;
        }
    }, { passive: false });

    // Navegação por clicar-e-arrastar (pan) nos eixos horizontal e vertical
    let dragging = false;
    let startX = 0, startY = 0, startLeft = 0, startTop = 0;

    scrollWrapper.style.cursor = 'grab';

    scrollWrapper.addEventListener('mousedown', function(event) {
        if (event.button !== 0) return;            // apenas o botão esquerdo
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

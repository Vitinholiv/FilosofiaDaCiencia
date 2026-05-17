var scrollWrapper = document.querySelector('.scroll-wrapper');

scrollWrapper.addEventListener('wheel', function(event) {
    if (event.deltaY !== 0) {
        event.preventDefault();
        scrollWrapper.scrollLeft += event.deltaY;
    }
}, { passive: false });
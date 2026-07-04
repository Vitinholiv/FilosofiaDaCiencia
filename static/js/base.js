import { setup_scroll } from './scroller.js';
import { TimelineApp } from './timeline.js';

document.addEventListener('DOMContentLoaded', function() {
    setup_scroll();
    TimelineApp.init();
});
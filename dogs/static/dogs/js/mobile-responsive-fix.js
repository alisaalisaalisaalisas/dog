/**
 * Mobile Optimization Script
 * Automatically fixes responsive issues for mobile devices
 */

(function () {
    'use strict';

    // Check if viewport is mobile
    function isMobileViewport() {
        return window.innerWidth <= 1024;
    }

    // Fix responsive issues on mobile
    function fixResponsiveIssues() {
        const isMobile = isMobileViewport();

        if (!isMobile) return;

        // Fix grid layouts that might be broken on mobile
        const gridContainers = document.querySelectorAll('[style*="grid-template-columns"]');
        gridContainers.forEach(container => {
            const style = container.getAttribute('style');

            // Check if it has a fixed column width that would cause issues
            if (style.includes('300px') || style.includes('400px') || style.includes('250px')) {
                // Already handled by CSS media queries
                // But we can ensure parent is not over-constrained
                if (container.parentElement) {
                    container.parentElement.style.width = '100%';
                    container.parentElement.style.overflowX = 'hidden';
                }
            }
        });

        // Ensure all cards are responsive
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            card.style.width = '100%';
        });

        // Ensure all rows are responsive
        const rows = document.querySelectorAll('.row, [style*="display: grid"]');
        rows.forEach(row => {
            // Only apply if it has problematic width
            const style = row.getAttribute('style');
            if (style && (style.includes('300px') || style.includes('400px'))) {
                row.style.width = '100%';
                row.style.display = 'block'; // Let CSS media queries handle
            }
        });

        // Fix elements with fixed widths
        const allElements = document.querySelectorAll('[style*="width: 300px"], [style*="width: 400px"], [style*="max-width: 1000px"], [style*="max-width: 1200px"]');
        allElements.forEach(el => {
            // Only force change if it would cause horizontal scroll
            const rect = el.getBoundingClientRect();
            if (rect.width > window.innerWidth - 40) { // 40px for padding
                el.style.width = '100%';
                el.style.maxWidth = '100%';
            }
        });
    }

    // Run on load and resize
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fixResponsiveIssues);
    } else {
        fixResponsiveIssues();
    }

    // Run on window resize with debounce
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(fixResponsiveIssues, 250);
    });

    // Also run on orientation change
    window.addEventListener('orientationchange', () => {
        setTimeout(fixResponsiveIssues, 100);
    });

    // Listen for dynamic content changes
    if ('MutationObserver' in window) {
        const observer = new MutationObserver((mutations) => {
            // Only check if changes might affect layout
            let hasLayoutChanges = false;
            mutations.forEach(mutation => {
                if (mutation.type === 'childList' || mutation.type === 'attributes') {
                    if (mutation.attributeName === 'style' || mutation.target.style) {
                        hasLayoutChanges = true;
                    }
                }
            });
            if (hasLayoutChanges && isMobileViewport()) {
                fixResponsiveIssues();
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['style'],
        });
    }

    // Prevent horizontal scroll
    function preventHorizontalScroll() {
        const body = document.body;
        if (body.scrollWidth > window.innerWidth) {
            // Find and log the culprit
            const elements = document.querySelectorAll('*');
            elements.forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.width > window.innerWidth) {
                    // Try to fix it
                    if (el.style.width && el.style.width.includes('px')) {
                        el.style.maxWidth = '100vw';
                    }
                    if (el.style.minWidth && el.style.minWidth.includes('px')) {
                        el.style.minWidth = 'auto';
                    }
                }
            });
        }
    }

    window.addEventListener('load', preventHorizontalScroll);
    window.addEventListener('resize', preventHorizontalScroll);

})();

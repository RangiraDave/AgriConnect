// Main Initialization
function initProductListings() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Filter auto-collapse
    initFilterAutoCollapse();
}

function initFilterAutoCollapse() {
    const filterCollapse = document.getElementById('filterCollapse');
    const filterHeader = document.getElementById('filterHeader');
    let filterTimeout;

    function resetFilterTimeout() {
        clearTimeout(filterTimeout);
        filterTimeout = setTimeout(() => {
            if (filterCollapse.classList.contains('show')) {
                bootstrap.Collapse.getInstance(filterCollapse).hide();
            }
        }, 5000);
    }

    // Reset timeout on any interaction with the filter form
    document.getElementById('filter-form').addEventListener('mouseover', resetFilterTimeout);
    document.getElementById('filter-form').addEventListener('mouseout', resetFilterTimeout);
    document.getElementById('filter-form').addEventListener('focusin', resetFilterTimeout);
    document.getElementById('filter-form').addEventListener('focusout', resetFilterTimeout);

    // Show filter on hover
    filterHeader.addEventListener('mouseover', function() {
        if (!filterCollapse.classList.contains('show')) {
            bootstrap.Collapse.getInstance(filterCollapse).show();
        }
        resetFilterTimeout();
    });

    // Update mobile detection on window resize
    window.addEventListener('resize', () => {
        const isMobile = window.innerWidth <= 768;
        if (isMobile) {
            filterHeader.addEventListener('click', (e) => {
                e.preventDefault();
                bootstrap.Collapse.getInstance(filterCollapse).toggle();
            });
        }
    });
}

// Initialize all components when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initLocationDropdowns();
    initRatingSystem();
    initChatbot();
    initProductListings();
});

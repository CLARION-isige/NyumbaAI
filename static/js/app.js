document.addEventListener('DOMContentLoaded', function() {
    // Auto-focus on search input
    const searchInput = document.querySelector('input[name="location"]');
    if (searchInput) {
        searchInput.focus();
    }

    // Handle form submission
    const searchForm = document.querySelector('form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const inputs = this.querySelectorAll('input');
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('is-invalid');
                } else {
                    input.classList.remove('is-invalid');
                }
            });
            
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
        });
    }

    // Add map integration placeholder
    if (document.querySelector('.listing-card')) {
        // Initialize map logic here
        console.log('Map integration ready');
    }
});
document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Initialize counters animation if present
    const counters = document.querySelectorAll('.counter');
    const speed = 200; // The lower the slower

    if (counters.length > 0) {
        // Simple Intersection Observer to trigger counting when visible
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = +counter.innerText;
                    
                    // Don't animate if it's not a valid number (like '∞')
                    if (isNaN(target)) return;
                    
                    let count = 0;
                    const updateCount = () => {
                        const inc = target / speed;
                        if (count < target) {
                            count += inc;
                            counter.innerText = Math.ceil(count);
                            setTimeout(updateCount, 1);
                        } else {
                            counter.innerText = target + (counter.dataset.suffix || '');
                        }
                    };
                    updateCount();
                    observer.unobserve(counter);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(counter => {
            if (!isNaN(+counter.innerText)) {
                observer.observe(counter);
            }
        });
    }

    // Initialize Masonry if grid exists (it will be handled mostly by the data attributes,
    // but this ensures it recalculates after images load)
    const galleryGrid = document.querySelector('#gallery');
    if (galleryGrid && window.Masonry) {
        // We assume imagesLoaded library isn't strictly required if aspect ratios are somewhat known,
        // but it's good practice to relayout on load
        window.addEventListener('load', () => {
            const msnry = Masonry.data(galleryGrid);
            if(msnry) msnry.layout();
        });
    }
});

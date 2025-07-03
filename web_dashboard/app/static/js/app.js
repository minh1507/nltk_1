// Main App JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Auto-close sidebar on mobile after clicking
    const sidebarLinks = document.querySelectorAll('#sidebar .nav-link');
    const sidebar = document.querySelector('#sidebar');
    
    if (window.innerWidth <= 768) {
        sidebarLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (!this.classList.contains('disabled')) {
                    const bsOffcanvas = bootstrap.Offcanvas.getInstance(sidebar);
                    if (bsOffcanvas) {
                        bsOffcanvas.hide();
                    }
                }
            });
        });
    }
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}); 
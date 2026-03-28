document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const body = document.body;

    // Create backdrop element for mobile menu
    let menuBackdrop = document.querySelector('.menu-backdrop');
    if (!menuBackdrop) {
        menuBackdrop = document.createElement('div');
        menuBackdrop.className = 'menu-backdrop';
        menuBackdrop.style.cssText = 'display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); z-index: 999; opacity: 0; transition: opacity 0.3s ease;';
        body.appendChild(menuBackdrop);
    }

    // Mobile menu toggle functionality
    if (mobileMenuToggle && navMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            const isActive = navMenu.classList.toggle('active');
            mobileMenuToggle.classList.toggle('active');
            
            if (isActive) {
                // Open menu
                menuBackdrop.style.display = 'block';
                setTimeout(() => menuBackdrop.style.opacity = '1', 10);
                body.classList.add('no-scroll');
            } else {
                // Close menu
                closeMobileMenu();
            }
        });

        // Close menu when clicking backdrop
        menuBackdrop.addEventListener('click', function() {
            closeMobileMenu();
        });

        // Close menu function
        function closeMobileMenu() {
            navMenu.classList.remove('active');
            mobileMenuToggle.classList.remove('active');
            menuBackdrop.style.opacity = '0';
            setTimeout(() => {
                menuBackdrop.style.display = 'none';
            }, 300);
            body.classList.remove('no-scroll');
        }

        // Close menu on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && navMenu.classList.contains('active')) {
                closeMobileMenu();
            }
        });

        // Mobile dropdown handling
        const dropdowns = navMenu.querySelectorAll('.dropdown');
        dropdowns.forEach(dropdown => {
            const dropdownLink = dropdown.querySelector('a');
            
            dropdownLink.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    dropdown.classList.toggle('active');
                }
            });
        });
    }

    // Close menu when clicking nav links (on mobile)
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Don't close if it's a dropdown toggle
            if (link.parentElement.classList.contains('dropdown') && window.innerWidth <= 768) {
                return;
            }
            
            if (window.innerWidth <= 768) {
                navMenu.classList.remove('active');
                mobileMenuToggle.classList.remove('active');
                menuBackdrop.style.opacity = '0';
                setTimeout(() => {
                    menuBackdrop.style.display = 'none';
                }, 300);
                body.classList.remove('no-scroll');
            }
        });
    });

    // Reset menu on resize to desktop
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            navMenu.classList.remove('active');
            mobileMenuToggle.classList.remove('active');
            menuBackdrop.style.display = 'none';
            body.classList.remove('no-scroll');
            
            // Reset mobile dropdowns
            const dropdowns = navMenu.querySelectorAll('.dropdown');
            dropdowns.forEach(dropdown => {
                dropdown.classList.remove('active');
            });
        }
    });

    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.feature-card, .practice-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Contact form success modal
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        if (window.location.hash === '#success') {
            showModal();
            history.replaceState(null, null, ' ');
        }
    }
});

function showModal() {
    const modal = document.getElementById('successModal');
    if (modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal() {
    const modal = document.getElementById('successModal');
    if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = 'auto';
    }
}

window.onclick = function(event) {
    const modal = document.getElementById('successModal');
    if (event.target === modal) {
        closeModal();
    }
}

function toggleArticle(articleId) {
    const article = document.getElementById(articleId);
    const button = event.target.closest('.article-read-more');
    
    if (!article || !button) return;
    
    if (article.style.display === 'none' || article.style.display === '') {
        article.style.display = 'block';
        button.textContent = 'Daha Az Göster ↑';
    } else {
        article.style.display = 'none';
        button.textContent = 'Devamını Oku →';
    }
}

// Toggle district cards (for calisma-bolgeleri.html)
function toggleDistrict(btn) {
    const card = btn.closest('.district-card');
    const fullContent = card.querySelector('.district-full-content');
    const span = btn.querySelector('span');
    
    if (fullContent.classList.contains('show')) {
        fullContent.classList.remove('show');
        btn.innerHTML = 'Devamını oku <span style="margin-left: 5px;">▼</span>';
    } else {
        fullContent.classList.add('show');
        btn.innerHTML = 'Daha az göster <span style="margin-left: 5px;">▲</span>';
    }
}

// Filter articles by category (for yayinlar.html)
function filterArticles(category) {
    const articles = document.querySelectorAll('.article-card');
    const buttons = document.querySelectorAll('.filter-btn');
    
    // Update active button state
    buttons.forEach(btn => {
        if (btn.getAttribute('data-filter') === category) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // Show/hide articles based on category
    articles.forEach(article => {
        const articleCategory = article.getAttribute('data-category');
        
        if (category === 'all') {
            article.style.display = 'block';
        } else if (articleCategory === category) {
            article.style.display = 'block';
        } else {
            article.style.display = 'none';
        }
    });
}

// Filter articles by category (for yayinlar.html)
function filterArticles(category) {
    const articles = document.querySelectorAll('.article-card');
    const buttons = document.querySelectorAll('.filter-btn');
    
    // Update active button state
    buttons.forEach(btn => {
        if (btn.getAttribute('data-filter') === category) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // Show/hide articles based on category
    articles.forEach(article => {
        const articleCategory = article.getAttribute('data-category');
        
        if (category === 'all') {
            article.style.display = 'block';
        } else if (articleCategory === category) {
            article.style.display = 'block';
        } else {
            article.style.display = 'none';
        }
    });
}

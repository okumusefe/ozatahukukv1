document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            mobileMenuToggle.classList.toggle('active');
        });
    }

    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                navMenu.classList.remove('active');
                mobileMenuToggle.classList.remove('active');
            }
        });
    });

    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            navMenu.classList.remove('active');
            mobileMenuToggle.classList.remove('active');
        }
    });

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
    const button = event.target;
    
    if (article.style.display === 'none') {
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

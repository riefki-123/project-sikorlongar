// Flash Message System
function showFlashMessage(type, message) {
  const flashContainer = document.getElementById('flashMessages');
  const flashMessage = document.createElement('div');
  flashMessage.className = `flash-message ${type}`;
  flashMessage.innerHTML = `
    <span>${message}</span>
    <button class="flash-close" onclick="closeFlashMessage(this)">×</button>
  `;
  
  flashContainer.appendChild(flashMessage);
  
  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (flashMessage.parentNode) {
      flashMessage.remove();
    }
  }, 5000);
}

function closeFlashMessage(button) {
  button.parentElement.remove();
}

// Count-up Animation for Statistics
function animateCountUp(element) {
  const target = parseInt(element.dataset.target);
  const duration = 2000; // 2 seconds
  const increment = target / (duration / 16); // 60 FPS
  let current = 0;
  
  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      element.textContent = target;
      clearInterval(timer);
    } else {
      element.textContent = Math.floor(current);
    }
  }, 16);
}

// Intersection Observer for Statistics Animation
function initStatsAnimation() {
  const statNumbers = document.querySelectorAll('.stat-number');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
        entry.target.classList.add('animated');
        animateCountUp(entry.target);
      }
    });
  }, { threshold: 0.5 });
  
  statNumbers.forEach(stat => {
    observer.observe(stat);
  });
}

// Search Form Handler
function initSearchForm() {
  const searchForm = document.getElementById('searchForm');
  const searchInput = document.getElementById('searchInput');
  
  searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const query = searchInput.value.trim();
    
    if (query) {
      showFlashMessage('info', `Searching for: "${query}"`);
      // Simulate search delay
      setTimeout(() => {
        showFlashMessage('success', 'Search completed! Results updated below.');
      }, 1500);
    } else {
      showFlashMessage('error', 'Please enter a search term');
    }
  });
}

// Smooth Scrolling for Internal Links
function initSmoothScrolling() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  initStatsAnimation();
  initSearchForm();
  initSmoothScrolling();
  
  // Show welcome message
  setTimeout(() => {
    showFlashMessage('info', 'Welcome to DisasterGuard - Your Emergency Response Information System');
  }, 1000);
});

// Additional Interactive Features
function handleTableRowClick() {
  const tableRows = document.querySelectorAll('.results-table tbody tr');
  
  tableRows.forEach(row => {
    row.addEventListener('click', () => {
      const name = row.cells[0].textContent;
      showFlashMessage('info', `Viewing details for ${name}`);
    });
  });
}

// Hero Section Parallax Effect (Optional Enhancement)
function initParallaxEffect() {
  window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    const rate = scrolled * -0.5;
    
    if (hero && scrolled < hero.offsetHeight) {
      hero.style.transform = `translate3d(0, ${rate}px, 0)`;
    }
  });
}

// Initialize additional features
document.addEventListener('DOMContentLoaded', () => {
  handleTableRowClick();
  
  // Uncomment the line below to enable parallax effect
  // initParallaxEffect();
});

// Utility function to format numbers with commas
function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Enhanced count-up animation with formatted numbers
function animateCountUpFormatted(element) {
  const target = parseInt(element.dataset.target);
  const duration = 2000;
  const increment = target / (duration / 16);
  let current = 0;
  
  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      element.textContent = formatNumber(target);
      clearInterval(timer);
    } else {
      element.textContent = formatNumber(Math.floor(current));
    }
  }, 16);
}
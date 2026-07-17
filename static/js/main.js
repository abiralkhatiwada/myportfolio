// Mobile navigation toggle
document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.getElementById("navToggle");
  const links = document.getElementById("navLinks");

  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("active");
      toggle.classList.toggle("open");
    });

    links.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        links.classList.remove("active");
        toggle.classList.remove("open");
      });
    });
  }

  // Navbar scroll effect
  const nav = document.getElementById("navbar");
  if (nav) {
    window.addEventListener("scroll", function () {
      if (window.scrollY > 50) {
        nav.style.background = "rgba(240, 240, 240, 0.95)";
        nav.style.backdropFilter = "blur(8px)";
        nav.style.webkitBackdropFilter = "blur(8px)";
        nav.style.boxShadow = "0 4px 0px #111111";
      } else {
        nav.style.background = "#FFFFFF";
        nav.style.backdropFilter = "none";
        nav.style.webkitBackdropFilter = "none";
        nav.style.boxShadow = "none";
      }
    });
  }

  // ========== PROJECTS SHOW MORE / SHOW LESS ==========
  const projectGrid = document.getElementById("projectGrid");
  const seeMoreWrapper = document.getElementById("seeMoreWrapper");
  const seeMoreBtn = document.getElementById("seeMoreBtn");

  if (projectGrid && seeMoreWrapper && seeMoreBtn) {
    const cards = Array.from(projectGrid.querySelectorAll(".project-card"));
    let isExpanded = false;

    function getVisibleLimit() {
      return window.innerWidth <= 768 ? 3 : 6;
    }

    function applyLimit() {
      const limit = getVisibleLimit();
      const hiddenCount = cards.length - limit;

      if (hiddenCount <= 0) {
        // Not enough cards to hide — hide the button, show all
        seeMoreWrapper.style.display = "none";
        cards.forEach(function (card) {
          card.classList.remove("hidden-card");
        });
        isExpanded = false;
        seeMoreBtn.classList.remove("expanded");
        seeMoreBtn.innerHTML = 'See More <span class="arrow-icon">↓</span>';
        return;
      }

      if (!isExpanded) {
        cards.forEach(function (card, i) {
          if (i >= limit) {
            card.classList.add("hidden-card");
          } else {
            card.classList.remove("hidden-card");
          }
        });
        seeMoreBtn.innerHTML = 'See More <span class="arrow-icon">↓</span>';
        seeMoreBtn.classList.remove("expanded");
      }

      seeMoreWrapper.style.display = "block";
    }

    seeMoreBtn.addEventListener("click", function () {
      isExpanded = !isExpanded;

      if (isExpanded) {
        cards.forEach(function (card) {
          card.classList.remove("hidden-card");
        });
        seeMoreBtn.innerHTML = 'Show Less <span class="arrow-icon">↓</span>';
        seeMoreBtn.classList.add("expanded");
      } else {
        applyLimit();
      }
    });

    // Re-apply on resize (e.g. rotating phone)
    let resizeTimer;
    window.addEventListener("resize", function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        // Reset expanded state on resize so limit recalculates correctly
        isExpanded = false;
        applyLimit();
      }, 150);
    });

    // Initial run
    applyLimit();
  }
});
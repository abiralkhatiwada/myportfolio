// Mobile navigation toggle
document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.getElementById("navToggle");
  const links = document.getElementById("navLinks");

  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("active");
      toggle.classList.toggle("open");
    });

    // Close menu when a link is clicked
    links.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        links.classList.remove("active");
        toggle.classList.remove("open");
      });
    });
  }

  // Navbar scroll effect (Updated for Neo-Brutalist Light Theme)
  const nav = document.getElementById("navbar");
  if (nav) {
    window.addEventListener("scroll", function () {
      if (window.scrollY > 50) {
        // Frosted glass effect matching the brutalist aesthetic
        nav.style.background = "rgba(240, 240, 240, 0.95)";
        nav.style.backdropFilter = "blur(8px)";
        nav.style.webkitBackdropFilter = "blur(8px)";
        // Hard offset shadow instead of a soft glow
        nav.style.boxShadow = "0 4px 0px #111111";
      } else {
        // Revert to clean white static state
        nav.style.background = "#FFFFFF";
        nav.style.backdropFilter = "none";
        nav.style.webkitBackdropFilter = "none";
        nav.style.boxShadow = "none";
      }
    });
  }
});

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

  // Navbar scroll effect
  const nav = document.getElementById("navbar");
  if (nav) {
    window.addEventListener("scroll", function () {
      if (window.scrollY > 50) {
        nav.style.background = "rgba(3, 7, 18, 0.95)";
        nav.style.boxShadow = "0 4px 32px rgba(0, 0, 0, 0.5)";
      } else {
        nav.style.background = "rgba(3, 7, 18, 0.82)";
        nav.style.boxShadow = "none";
      }
    });
  }
});

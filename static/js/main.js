// Mobile navigation toggle
document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.getElementById("navToggle");
  const links = document.getElementById("navLinks");

  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("active");
    });

    // Close menu when a link is clicked
    links.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        links.classList.remove("active");
      });
    });
  }

  // Navbar scroll effect
  const nav = document.getElementById("navbar");
  if (nav) {
    window.addEventListener("scroll", function () {
      if (window.scrollY > 50) {
        nav.style.background = "rgba(15, 23, 42, 0.95)";
        nav.style.boxShadow = "0 4px 20px rgba(0, 0, 0, 0.3)";
      } else {
        nav.style.background = "rgba(15, 23, 42, 0.85)";
        nav.style.boxShadow = "none";
      }
    });
  }
});

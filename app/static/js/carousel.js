let current = 0;

// Direct image list – change if needed
const images = [
  "/static/Aatrox.jpg",
  "/static/Jinx.jpg",
  "/static/Lux.jpg"
];

function showSlide(index) {
  const bgImg = document.getElementById("bg-img");
  if (!bgImg) return;

  current = (index + images.length) % images.length;
  bgImg.style.opacity = 0;

  // Wait for opacity animation before changing image
  setTimeout(() => {
    bgImg.src = images[current];
    bgImg.style.opacity = 1;
  }, 200);
}

// Global functions for HTML
function prevslide() {
  showSlide(current - 1);
}

function nextslide() {
  showSlide(current + 1);
}

// Expose to global scope
window.prevslide = prevslide;
window.nextslide = nextslide;





    
  




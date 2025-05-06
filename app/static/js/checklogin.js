document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.protected-link').forEach(link => {
      link.addEventListener('click', event => {
        if (isUserLoggedIn === 'false') {
          event.preventDefault();
          alert("Please login to access this page!");
        } else {
          window.location.href = link.dataset.url;
        }
      });
    });
  });
  
  
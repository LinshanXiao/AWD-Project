document.addEventListener('DOMContentLoaded', function () {
    const dropdownBtn = document.querySelector('.dropdown-btn');
    const dropdownContent = document.querySelector('.dropdown-content');
  
    dropdownBtn.addEventListener('click', function () {
      // Toggle dropdown visibility
      if (dropdownContent.style.display === 'flex') {
        dropdownContent.style.display = 'none';
      } else {
        dropdownContent.style.display = 'flex';
        dropdownContent.style.flexDirection = 'column';
      }
    });
  });
  
  
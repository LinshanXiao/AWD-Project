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


  const avatar = document.getElementById('userAvatar');
  const dropdown = document.getElementById('dropdownMenu');

  avatar.addEventListener('click', function (e) {
    e.stopPropagation();
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
  });

  document.addEventListener('click', function () {
    dropdown.style.display = 'none';
  });
  
  
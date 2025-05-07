document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById('searchInput');
    const resultsBox = document.getElementById('searchResults');
    let timeout = null;
  
    input.addEventListener('input', () => {
      clearTimeout(timeout);
      const query = input.value.trim();
      if (!query) {
        resultsBox.style.display = 'none';
        return;
      }
  
      // add a slight delay to avoid sending too much request while typing 
      timeout = setTimeout(async () => {
        const response = await fetch(`/api/search_user?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        resultsBox.style.display = 'block';
  
        if (data.found) {
          resultsBox.innerHTML = `
            <div class="dropdown-item">
              ${data.username} (ID: ${data.id})
              <button onclick="addFriend(${data.id})">Add Friend</button>
            </div>`;
        } else {
          resultsBox.innerHTML = "<div class='dropdown-item'>User not found.</div>";
        }
      }, 300);  // delay 300ms to rebounce
    });
  
    // hide search results when clicking outside the search box 
    document.addEventListener('click', (e) => {
      if (!document.querySelector('.search-box').contains(e.target)) {
        resultsBox.style.display = 'none';
      }
    });
  });
  
  async function addFriend(userId) {
    const response = await fetch('/add_friend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ friend_id: userId })
    });
  
    const result = await response.json();
    alert(result.message);  // success or failed to add
  }
  
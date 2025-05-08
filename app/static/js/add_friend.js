document.addEventListener("click", function (event) {
    if (event.target.classList.contains("add-friend-btn")) {
        const userId = event.target.dataset.userid;

        fetch("/add_friend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest"
            },
            body: JSON.stringify({ user_id: userId })
        })
        .then(res => res.json())
        .then(data => {
            alert(data.message);
        })
        .catch(err => {
            alert("Failed to add friend.");
            console.error(err);
        });
    }
});

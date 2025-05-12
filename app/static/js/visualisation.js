document.addEventListener('DOMContentLoaded', async () => {
    // Fetch game data from Flask
    const response = await fetch('/visualisation/data');
    const data = await response.json();

    // --- Chart 1: Champion Win Rates ---
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.champion_names,
            datasets: [{
                label: 'Champion Win Rates (%)',
                data: data.win_rates,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Champion Win Rates (%)'
                },
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    // --- Chart 2: Score Over Time ---
    const lineCtx = document.getElementById('lineChart').getContext('2d');
    new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: data.score_labels, 
            datasets: [{
                label: 'Scores Over Time',
                data: data.scores,
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderWidth: 2,
                tension: 0.3
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Scores Over Time'
                }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
});

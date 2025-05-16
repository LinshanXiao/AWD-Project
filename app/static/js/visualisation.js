document.addEventListener('DOMContentLoaded', function () {
    const jsonEl = document.getElementById('chart-data');
    if (!jsonEl) {
        console.error("chart-data <script> tag not found.");
        return;
    }

    let chartData;
    try {
        chartData = JSON.parse(jsonEl.textContent);
    } catch (e) {
        console.error("Failed to parse chart data JSON:", e);
        return;
    }

    // === Champion Usage (Bar Chart) ===
    const ctxBar = document.getElementById('championBarChart');
    if (ctxBar && chartData.championCounts) {
        new Chart(ctxBar.getContext('2d'), {
            type: 'bar',
            data: {
                labels: Object.keys(chartData.championCounts),
                datasets: [{
                    label: 'Times Played',
                    data: Object.values(chartData.championCounts),
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }

    // === Champion Win Rate (Pie Chart) ===
    const ctxPie = document.getElementById('championPieChart');
    if (ctxPie && chartData.winRates) {
        new Chart(ctxPie.getContext('2d'), {
            type: 'pie',
            data: {
                labels: Object.keys(chartData.winRates),
                datasets: [{
                    label: 'Win Rate (%)',
                    data: Object.values(chartData.winRates),
                    backgroundColor: Object.keys(chartData.winRates).map((_, i) =>
                        `hsl(${i * 50}, 70%, 60%)`
                    ),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true
            }
        });
    }

    // === Performance Radar Chart ===
    const ctxRadar = document.getElementById('performanceRadar');
    if (ctxRadar && chartData.radarData) {
        const labels = Object.keys(chartData.radarData);
        const values = Object.values(chartData.radarData);

        new Chart(ctxRadar.getContext('2d'), {
    type: 'radar',
    data: {
        labels: labels,
        datasets: [{
            label: 'Recent Game Performance',
            data: values,
            fill: true,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: '#ff4c70',  
            borderWidth: 3,          
            pointBackgroundColor: '#ff4c70',
            pointBorderColor: '#fff'
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                labels: {
                    color: '#ffffff'
                }
            }
        },
        scales: {
            r: {
                angleLines: {
                    color: '#555'
                },
                grid: {
                    color: '#444'
                },
                pointLabels: {
                    color: '#fff',
                    font: {
                        size: 14
                    }
                },
                ticks: {
                    display: false  
                },
                suggestedMin: 0,
                suggestedMax: 10
            }
        }
    }
});
    }
});

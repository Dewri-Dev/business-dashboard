/**
 * Trend Analysis Visualizer
 * Uses Chart.js to render business history
 */

let businessChart = null;

function updateTrendsChart(data) {
    const ctx = document.getElementById('trendsChart').getContext('2d');
    
    const labels = data.map(item => item.date);
    const revenueData = data.map(item => item.revenue);
    const expenseData = data.map(item => item.expenses);

    if (businessChart) {
        businessChart.destroy();
    }

    businessChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Revenue',
                    data: revenueData,
                    borderColor: '#38bdf8',
                    backgroundColor: 'rgba(56, 189, 248, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Expenses',
                    data: expenseData,
                    borderColor: '#f43f5e',
                    backgroundColor: 'transparent',
                    borderDash: [5, 5],
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#94a3b8', font: { family: 'Inter' } }
                }
            },
            scales: {
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            }
        }
    });
}
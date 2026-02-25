/**
 * Main Dashboard Controller
 * Orchestrates real-time data fetching and UI updates
 */

const API_BASE = "http://127.0.0.1:5000";

document.addEventListener('DOMContentLoaded', () => {
    refreshDashboard();
    
    // Form Submission
    document.getElementById('dataForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const payload = {
            date: document.getElementById('date').value,
            revenue: parseFloat(document.getElementById('revenue').value),
            expenses: parseFloat(document.getElementById('expenses').value),
            inventory_cost: parseFloat(document.getElementById('inventory').value),
            category: document.getElementById('category').value
        };

        try {
            const response = await fetch(`${API_BASE}/add-data`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                toggleModal();
                document.getElementById('dataForm').reset();
                refreshDashboard();
            } else {
                const err = await response.json();
                alert(`Error: ${err.error}`);
            }
        } catch (error) {
            console.error("Submission failed:", error);
        }
    });
});

async function refreshDashboard() {
    try {
        // Fetch Summary Metrics
        const sumRes = await fetch(`${API_BASE}/summary`);
        const summary = await sumRes.json();
        updateStatsUI(summary);
        
        // Update Alerts
        if (typeof renderAlerts === 'function') {
            renderAlerts(summary.alerts);
        }

        // Fetch Trends & Update Chart
        const trendRes = await fetch(`${API_BASE}/trends`);
        const trends = await trendRes.json();
        if (typeof updateTrendsChart === 'function') {
            updateTrendsChart(trends);
        }
    } catch (err) {
        console.error("Failed to refresh dashboard:", err);
    }
}

function updateStatsUI(data) {
    const { metrics, health_score } = data;
    
    // Animate numbers (simple version)
    document.getElementById('stat-revenue').innerText = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(metrics.total_revenue);
    document.getElementById('stat-profit').innerText = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(metrics.net_profit);
    document.getElementById('stat-margin').innerText = `${metrics.profit_margin}%`;
    document.getElementById('stat-health').innerText = health_score;
    
    // Update health bar
    const bar = document.getElementById('health-bar');
    bar.style.width = `${health_score}%`;
    
    // Color coding
    if (health_score < 40) bar.className = "bg-rose-500 h-full transition-all duration-1000";
    else if (health_score < 70) bar.className = "bg-amber-500 h-full transition-all duration-1000";
    else bar.className = "bg-emerald-500 h-full transition-all duration-1000";
}

function toggleModal() {
    const modal = document.getElementById('modal');
    modal.classList.toggle('hidden');
}
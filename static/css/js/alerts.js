/**
 * Smart Alert Parser
 * Displays warnings and health notifications
 */

function renderAlerts(alerts) {
    const container = document.getElementById('alerts-container');
    container.innerHTML = ''; // Clear current

    alerts.forEach(msg => {
        const div = document.createElement('div');
        
        // Determine alert style
        let bgColor = "bg-slate-800/50";
        let iconColor = "text-sky-400";
        let iconType = "info";

        if (msg.includes("CRITICAL")) {
            bgColor = "bg-rose-500/10 border border-rose-500/20";
            iconColor = "text-rose-500";
            iconType = "alert-octagon";
        } else if (msg.includes("WARNING")) {
            bgColor = "bg-amber-500/10 border border-amber-500/20";
            iconColor = "text-amber-500";
            iconType = "alert-triangle";
        }

        div.className = `${bgColor} p-4 rounded-xl text-sm flex items-start space-x-3`;
        div.innerHTML = `
            <i data-lucide="${iconType}" class="${iconColor} w-5 h-5 flex-shrink-0"></i>
            <span class="leading-snug">${msg}</span>
        `;
        
        container.appendChild(div);
    });

    // Re-initialize icons for newly added elements
    if (window.lucide) {
        window.lucide.createIcons();
    }
}
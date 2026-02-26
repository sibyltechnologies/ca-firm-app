// CA Firm Management — Global JS helpers
frappe.provide("ca_firm");

ca_firm.risk_colors = {
    "Low": "green",
    "Medium": "yellow",
    "High": "orange",
    "Very High": "red",
};

ca_firm.status_colors = {
    "Planning": "blue",
    "In Progress": "yellow",
    "Under Review": "orange",
    "Pending Client": "purple",
    "Completed": "green",
    "Billed": "teal",
    "Cancelled": "red",
};

// Helper: format PKR currency
ca_firm.fmt_pkr = function(amount) {
    return "PKR " + frappe.utils.fmt_money(amount || 0);
};

// Helper: days indicator badge
ca_firm.days_badge = function(days) {
    if (days === null || days === undefined) return "";
    if (days < 0) return `<span class="badge badge-danger">Overdue ${Math.abs(days)}d</span>`;
    if (days <= 7) return `<span class="badge badge-warning">${days}d left</span>`;
    return `<span class="badge badge-success">${days}d left</span>`;
};

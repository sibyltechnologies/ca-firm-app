import frappe


def format_engagement_id(name):
    """Jinja helper for templates"""
    return name or ""


def get_risk_badge(risk_rating):
    """Return HTML badge for risk rating"""
    colors = {
        "Low": "#28a745",
        "Medium": "#ffc107",
        "High": "#fd7e14",
        "Very High": "#dc3545",
    }
    color = colors.get(risk_rating, "#6c757d")
    return f'<span style="background:{color};color:white;padding:2px 8px;border-radius:3px;font-size:11px">{risk_rating}</span>'


@frappe.whitelist()
def get_dashboard_stats():
    """Global dashboard stats for the home page"""
    active_clients = frappe.db.count("CA Client", {"status": "Active"})
    active_engagements = frappe.db.count(
        "CA Engagement", {"status": ["in", ["Planning", "In Progress", "Under Review"]]}
    )
    overdue_invoices = frappe.db.count("CA Invoice", {"payment_status": "Overdue", "docstatus": 1})
    
    total_billed = frappe.db.sql(
        "SELECT SUM(total_amount) FROM `tabCA Invoice` WHERE docstatus=1 AND payment_status='Paid'"
    )[0][0] or 0
    
    total_outstanding = frappe.db.sql(
        "SELECT SUM(total_amount) FROM `tabCA Invoice` WHERE docstatus=1 AND payment_status IN ('Unpaid','Overdue','Partially Paid')"
    )[0][0] or 0

    return {
        "active_clients": active_clients,
        "active_engagements": active_engagements,
        "overdue_invoices": overdue_invoices,
        "total_billed": total_billed,
        "total_outstanding": total_outstanding,
    }

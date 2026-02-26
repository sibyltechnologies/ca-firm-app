import frappe


def client_dashboard(data):
    return {
        "fieldname": "name",
        "transactions": [
            {"label": "Engagements", "items": ["CA Engagement"]},
            {"label": "Invoices", "items": ["CA Invoice"]},
            {"label": "Timesheets", "items": ["CA Timesheet Entry"]},
            {"label": "Contact Logs", "items": ["CA Contact Log"]},
        ],
    }

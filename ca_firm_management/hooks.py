app_name = "ca_firm_management"
app_title = "CA Firm Management"
app_publisher = "Sibyl Technologies"
app_description = "CA Firm Practice Management System"
app_email = "support@sibyl.pk"
app_license = "GPL-3.0"
app_version = "1.0.0"

# ─── Fixtures (to export config with the app) ─────────────────────────────────
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [["module", "in", ["CA Firm Management"]]]
    },
    {
        "doctype": "Property Setter",
        "filters": [["module", "in", ["CA Firm Management"]]]
    },
    {
        "doctype": "Role",
        "filters": [["name", "in", [
            "CA Partner",
            "CA Manager",
            "CA Senior",
            "CA Trainee",
            "CA Admin",
        ]]]
    }
]

# ─── App-wide CSS / JS ────────────────────────────────────────────────────────
app_include_css = ["ca_firm_management.bundle.css"]
app_include_js  = ["ca_firm_management.bundle.js"]
# ─── Doc Events ───────────────────────────────────────────────────────────────
doc_events = {
    "CA Engagement": {
        "on_submit":  "ca_firm_management.events.engagement.on_submit",
        "on_cancel":  "ca_firm_management.events.engagement.on_cancel",
        "before_save": "ca_firm_management.events.engagement.before_save",
    },
    "CA Timesheet Entry": {
        "before_save": "ca_firm_management.events.timesheet.before_save",
    }
}

# ─── Scheduled Tasks ──────────────────────────────────────────────────────────
scheduler_events = {
    "daily": [
        "ca_firm_management.tasks.send_deadline_reminders",
        "ca_firm_management.tasks.update_engagement_status",
    ],
    "weekly": [
        "ca_firm_management.tasks.generate_utilization_report",
    ]
}

# ─── Permissions ──────────────────────────────────────────────────────────────
# Override standard list view for CA docTypes
override_doctype_dashboards = {
    "CA Client": "ca_firm_management.dashboard.client_dashboard",
}

# ─── Website / Portal (future use) ───────────────────────────────────────────
website_route_rules = []

# ─── Jinja env ────────────────────────────────────────────────────────────────
jinja = {
    "methods": [
        "ca_firm_management.utils.format_engagement_id",
        "ca_firm_management.utils.get_risk_badge",
    ]
}

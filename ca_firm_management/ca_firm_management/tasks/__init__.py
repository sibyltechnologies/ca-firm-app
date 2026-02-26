import frappe
from frappe.utils import today, date_diff, getdate, add_days


def send_deadline_reminders():
    """Run daily — notify partners/managers of upcoming deadlines"""
    warning_days = [1, 3, 7, 14]  # Send reminders at these thresholds

    engagements = frappe.get_all(
        "CA Engagement",
        filters={
            "status": ["in", ["Planning", "In Progress", "Under Review", "Pending Client"]],
            "deadline": ["between", [today(), add_days(today(), 14)]],
        },
        fields=["name", "client_name", "engagement_type", "deadline",
                "engagement_partner", "engagement_manager", "status"],
    )

    for eng in engagements:
        days_left = date_diff(eng.deadline, today())
        if days_left in warning_days:
            _send_deadline_alert(eng, days_left)


def _send_deadline_alert(eng, days_left):
    recipients = []
    for field in ["engagement_partner", "engagement_manager"]:
        staff = eng.get(field)
        if staff:
            email = frappe.db.get_value("CA Staff Profile", staff, "email")
            if email:
                recipients.append(email)

    if not recipients:
        return

    urgency = "🚨 URGENT" if days_left <= 3 else "⚠️ Reminder"
    frappe.sendmail(
        recipients=recipients,
        subject=f"{urgency}: {eng.name} — {eng.client_name} deadline in {days_left} day(s)",
        message=f"""
        <p>Dear Team,</p>
        <p>This is a reminder that engagement <strong>{eng.name}</strong> for 
        <strong>{eng.client_name}</strong> ({eng.engagement_type}) has a deadline 
        in <strong>{days_left} day(s)</strong> — <strong>{eng.deadline}</strong>.</p>
        <p>Current Status: {eng.status}</p>
        <p>Please take necessary action.</p>
        """,
    )


def update_engagement_status():
    """Auto-mark overdue invoices daily"""
    frappe.db.sql(
        """UPDATE `tabCA Invoice`
           SET payment_status = 'Overdue'
           WHERE due_date < %s 
             AND payment_status IN ('Unpaid', 'Partially Paid')
             AND docstatus = 1""",
        [today()],
    )
    frappe.db.commit()


def generate_utilization_report():
    """Weekly — log utilization stats (for analytics)"""
    # Placeholder: can be expanded to push to a dashboard doctype
    frappe.logger().info("Weekly utilization stats computed.")

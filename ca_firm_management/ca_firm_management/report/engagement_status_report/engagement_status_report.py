import frappe
from frappe.utils import today, date_diff


def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Engagement", "fieldname": "name", "fieldtype": "Link", "options": "CA Engagement", "width": 130},
        {"label": "Client", "fieldname": "client_name", "fieldtype": "Data", "width": 180},
        {"label": "Type", "fieldname": "engagement_type", "fieldtype": "Data", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 110},
        {"label": "Partner", "fieldname": "engagement_partner", "fieldtype": "Link", "options": "CA Staff Profile", "width": 130},
        {"label": "Manager", "fieldname": "engagement_manager", "fieldtype": "Link", "options": "CA Staff Profile", "width": 130},
        {"label": "Deadline", "fieldname": "deadline", "fieldtype": "Date", "width": 100},
        {"label": "Days Left", "fieldname": "days_left", "fieldtype": "Int", "width": 80},
        {"label": "Progress %", "fieldname": "progress_percent", "fieldtype": "Percent", "width": 90},
        {"label": "Fee (PKR)", "fieldname": "fee_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Billing Status", "fieldname": "billing_status", "fieldtype": "Data", "width": 110},
        {"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 80},
    ]


def get_data(filters):
    conditions = []
    values = {}

    if filters.get("client"):
        conditions.append("client = %(client)s")
        values["client"] = filters["client"]
    if filters.get("status"):
        conditions.append("status = %(status)s")
        values["status"] = filters["status"]
    if filters.get("engagement_type"):
        conditions.append("engagement_type = %(engagement_type)s")
        values["engagement_type"] = filters["engagement_type"]
    if filters.get("engagement_partner"):
        conditions.append("engagement_partner = %(engagement_partner)s")
        values["engagement_partner"] = filters["engagement_partner"]

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    rows = frappe.db.sql(
        f"""
        SELECT name, client_name, engagement_type, status, 
               engagement_partner, engagement_manager, deadline, 
               progress_percent, fee_amount, billing_status, priority
        FROM `tabCA Engagement`
        {where}
        ORDER BY deadline ASC
        """,
        values,
        as_dict=True,
    )

    for row in rows:
        if row.deadline:
            row["days_left"] = date_diff(row.deadline, today())
        else:
            row["days_left"] = None

    return rows

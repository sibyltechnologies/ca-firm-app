import frappe
from frappe.utils import get_first_day, get_last_day, today


def execute(filters=None):
    filters = filters or {}
    if not filters.get("month"):
        filters["month"] = today()[:7]

    month_start = get_first_day(filters["month"] + "-01")
    month_end = get_last_day(filters["month"] + "-01")

    columns = [
        {"label": "Staff", "fieldname": "staff_name", "fieldtype": "Data", "width": 180},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "width": 140},
        {"label": "Hours Logged", "fieldname": "hours_logged", "fieldtype": "Float", "width": 110},
        {"label": "Target Hours", "fieldname": "target_hours", "fieldtype": "Int", "width": 100},
        {"label": "Utilization %", "fieldname": "utilization_pct", "fieldtype": "Percent", "width": 100},
        {"label": "Billable Hours", "fieldname": "billable_hours", "fieldtype": "Float", "width": 110},
        {"label": "Billable Amount", "fieldname": "billable_amount", "fieldtype": "Currency", "width": 140},
        {"label": "Engagements", "fieldname": "engagements", "fieldtype": "Int", "width": 100},
    ]

    staff_list = frappe.get_all(
        "CA Staff Profile",
        filters={"is_active": 1},
        fields=["name", "full_name", "designation", "monthly_target_hours"],
    )

    rows = []
    for s in staff_list:
        result = frappe.db.sql(
            """
            SELECT 
                SUM(hours_logged) as total_hours,
                SUM(CASE WHEN is_billable = 1 THEN hours_logged ELSE 0 END) as billable_hours,
                SUM(billable_amount) as billable_amount,
                COUNT(DISTINCT engagement) as engagements
            FROM `tabCA Timesheet Entry`
            WHERE staff_member = %s
              AND work_date BETWEEN %s AND %s
              AND docstatus != 2
            """,
            [s.name, month_start, month_end],
            as_dict=True,
        )[0]

        target = s.monthly_target_hours or 160
        logged = result.total_hours or 0
        util = round((logged / target) * 100, 1) if target else 0

        rows.append({
            "staff_name": s.full_name,
            "designation": s.designation,
            "hours_logged": logged,
            "target_hours": target,
            "utilization_pct": util,
            "billable_hours": result.billable_hours or 0,
            "billable_amount": result.billable_amount or 0,
            "engagements": result.engagements or 0,
        })

    rows.sort(key=lambda x: x["utilization_pct"], reverse=True)
    return columns, rows

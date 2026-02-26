import frappe
from frappe.utils import getdate


def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": "Invoice", "fieldname": "name", "fieldtype": "Link", "options": "CA Invoice", "width": 130},
        {"label": "Client", "fieldname": "client_name", "fieldtype": "Data", "width": 180},
        {"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "CA Engagement", "width": 130},
        {"label": "Invoice Date", "fieldname": "invoice_date", "fieldtype": "Date", "width": 100},
        {"label": "Due Date", "fieldname": "due_date", "fieldtype": "Date", "width": 100},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
        {"label": "Tax", "fieldname": "tax_amount", "fieldtype": "Currency", "width": 100},
        {"label": "Total", "fieldname": "total_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Status", "fieldname": "payment_status", "fieldtype": "Data", "width": 110},
        {"label": "Payment Date", "fieldname": "payment_date", "fieldtype": "Date", "width": 100},
    ]

    conditions = ["docstatus = 1"]
    values = {}

    if filters.get("client"):
        conditions.append("client = %(client)s")
        values["client"] = filters["client"]
    if filters.get("payment_status"):
        conditions.append("payment_status = %(payment_status)s")
        values["payment_status"] = filters["payment_status"]
    if filters.get("from_date"):
        conditions.append("invoice_date >= %(from_date)s")
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions.append("invoice_date <= %(to_date)s")
        values["to_date"] = filters["to_date"]

    where = "WHERE " + " AND ".join(conditions)

    data = frappe.db.sql(
        f"""SELECT name, client_name, engagement, invoice_date, due_date,
               amount, tax_amount, total_amount, payment_status, payment_date
            FROM `tabCA Invoice` {where} ORDER BY invoice_date DESC""",
        values, as_dict=True,
    )
    return columns, data

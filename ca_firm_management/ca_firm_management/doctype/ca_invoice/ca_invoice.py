import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate, date_diff, add_days


class CAInvoice(Document):
    def validate(self):
        self._calculate_tax()
        self._set_due_date()
        self._check_overdue()

    def _calculate_tax(self):
        engagement = frappe.db.get_value("CA Engagement", self.engagement, "tax_applicable") if self.engagement else None
        if engagement:
            self.tax_amount = round(float(self.amount or 0) * 0.16, 2)
        else:
            self.tax_amount = 0
        self.total_amount = (self.amount or 0) + self.tax_amount

    def _set_due_date(self):
        if not self.due_date and self.invoice_date:
            self.due_date = add_days(self.invoice_date, 30)

    def _check_overdue(self):
        if (
            self.due_date
            and getdate(self.due_date) < getdate(today())
            and self.payment_status in ("Unpaid", "Partially Paid")
        ):
            self.payment_status = "Overdue"

    def on_submit(self):
        # Update engagement billing status
        if self.engagement:
            frappe.db.set_value("CA Engagement", self.engagement, "billing_status", "Fully Billed")
            frappe.db.set_value("CA Engagement", self.engagement, "status", "Billed")

    def on_cancel(self):
        if self.engagement:
            frappe.db.set_value("CA Engagement", self.engagement, "billing_status", "Unbilled")

    @frappe.whitelist()
    def mark_paid(self, payment_date=None, payment_reference=None, payment_method=None):
        self.db_set("payment_status", "Paid")
        self.db_set("payment_date", payment_date or today())
        if payment_reference:
            self.db_set("payment_reference", payment_reference)
        if payment_method:
            self.db_set("payment_method", payment_method)
        frappe.msgprint(f"Invoice {self.name} marked as Paid.", indicator="green", alert=True)

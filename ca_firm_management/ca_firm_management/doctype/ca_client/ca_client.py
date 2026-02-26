import frappe
from frappe.model.document import Document
from frappe.utils import today


class CAClient(Document):
    def autoname(self):
        if not self.client_code:
            self.client_code = self._generate_client_code()

    def _generate_client_code(self):
        """Auto-generate code like CLT-2024-001"""
        year = frappe.utils.nowdate()[:4]
        last = frappe.db.sql(
            """SELECT MAX(CAST(SUBSTRING_INDEX(client_code, '-', -1) AS UNSIGNED))
               FROM `tabCA Client`
               WHERE client_code LIKE %s""",
            [f"CLT-{year}-%"],
        )
        num = (last[0][0] or 0) + 1
        return f"CLT-{year}-{str(num).zfill(3)}"

    def validate(self):
        self._validate_ntn()
        self._set_risk_defaults()

    def _validate_ntn(self):
        if self.ntn:
            # Basic NTN format check (Pakistan 7-digit)
            ntn_clean = self.ntn.replace("-", "").replace(" ", "")
            if not ntn_clean.isdigit():
                frappe.throw("NTN must be numeric digits only.")

    def _set_risk_defaults(self):
        if not self.risk_rating:
            self.risk_rating = "Low"

    def on_update(self):
        self._log_risk_change()

    def _log_risk_change(self):
        """Log when risk rating changes — audit trail"""
        doc_before = self.get_doc_before_save()
        if doc_before and doc_before.risk_rating != self.risk_rating:
            frappe.get_doc({
                "doctype": "CA Contact Log",
                "client": self.name,
                "log_type": "Risk Change",
                "notes": f"Risk rating changed from {doc_before.risk_rating} to {self.risk_rating}",
                "log_date": today(),
                "logged_by": frappe.session.user,
            }).insert(ignore_permissions=True)

    @frappe.whitelist()
    def get_engagement_summary(self):
        """Return summary stats for dashboard"""
        engagements = frappe.get_all(
            "CA Engagement",
            filters={"client": self.name},
            fields=["name", "engagement_type", "status", "fee_amount", "deadline"],
        )
        total_billed = frappe.db.sql(
            """SELECT SUM(total_amount) FROM `tabCA Invoice`
               WHERE client = %s AND docstatus = 1""",
            [self.name],
        )
        return {
            "engagements": engagements,
            "total_billed": (total_billed[0][0] or 0),
            "active_count": sum(1 for e in engagements if e.status == "In Progress"),
        }

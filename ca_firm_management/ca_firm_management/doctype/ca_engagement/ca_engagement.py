import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate, date_diff, nowdate


class CAEngagement(Document):
    def validate(self):
        self._validate_dates()
        self._validate_team()
        self._warn_missing_engagement_letter()
        self._auto_set_financial_year()

    def _validate_dates(self):
        if self.period_from and self.period_to:
            if getdate(self.period_from) > getdate(self.period_to):
                frappe.throw("Period From cannot be after Period To.")
        if self.deadline and getdate(self.deadline) < getdate(today()):
            if self.status not in ("Completed", "Cancelled", "Billed"):
                frappe.msgprint(
                    f"⚠️ Deadline {self.deadline} is in the past.",
                    indicator="orange",
                    alert=True,
                )

    def _validate_team(self):
        if self.engagement_partner and self.engagement_manager:
            if self.engagement_partner == self.engagement_manager:
                frappe.throw("Engagement Partner and Manager cannot be the same person.")

    def _warn_missing_engagement_letter(self):
        if self.status == "In Progress" and not self.engagement_letter_received:
            frappe.msgprint(
                "Engagement Letter not yet received. Ensure it is obtained before proceeding.",
                indicator="yellow",
                alert=True,
            )

    def _auto_set_financial_year(self):
        if not self.financial_year and self.period_from:
            d = getdate(self.period_from)
            # Pakistan FY: July-June
            if d.month >= 7:
                self.financial_year = f"{d.year}-{str(d.year + 1)[2:]}"
            else:
                self.financial_year = f"{d.year - 1}-{str(d.year)[2:]}"

    def before_submit(self):
        """Validations before submission (locks document)"""
        if not self.engagement_letter_received:
            frappe.throw("Engagement Letter must be received before submitting the engagement.")
        if not self.terms_agreed:
            frappe.throw("Terms & Conditions must be agreed before submission.")
        if not self.fee_amount or self.fee_amount <= 0:
            frappe.throw("Fee Amount must be set before submission.")

    def on_submit(self):
        self._notify_team()

    def _notify_team(self):
        """Send email notifications to assigned team"""
        recipients = []
        for field in ["engagement_partner", "engagement_manager", "senior_in_charge"]:
            staff = getattr(self, field, None)
            if staff:
                email = frappe.db.get_value("CA Staff Profile", staff, "email")
                if email:
                    recipients.append(email)
        if recipients:
            frappe.sendmail(
                recipients=recipients,
                subject=f"New Engagement Confirmed: {self.name} — {self.client_name}",
                message=f"""
                <p>Dear Team,</p>
                <p>Engagement <strong>{self.name}</strong> for <strong>{self.client_name}</strong>
                ({self.engagement_type}) has been confirmed.</p>
                <p><strong>Deadline:</strong> {self.deadline or 'Not set'}</p>
                <p><strong>Fee:</strong> PKR {frappe.utils.fmt_money(self.fee_amount)}</p>
                <p>Please log in to the system to review assignment details.</p>
                """,
            )

    def on_cancel(self):
        # Cancel any linked unpaid invoices
        invoices = frappe.get_all(
            "CA Invoice",
            filters={"engagement": self.name, "docstatus": 0},
            fields=["name"],
        )
        for inv in invoices:
            frappe.get_doc("CA Invoice", inv.name).cancel()

    @frappe.whitelist()
    def get_days_to_deadline(self):
        if not self.deadline:
            return None
        return date_diff(self.deadline, today())

    @frappe.whitelist()
    def mark_complete(self):
        """Quick complete action"""
        self.db_set("status", "Completed")
        self.db_set("progress_percent", 100)
        self.db_set("completion_date", today())
        self.db_set("closed_by", frappe.session.user)
        frappe.msgprint("Engagement marked as Completed.", indicator="green", alert=True)

    @frappe.whitelist()
    def get_timesheet_summary(self):
        """Summarize logged hours for this engagement"""
        result = frappe.db.sql(
            """
            SELECT 
                s.staff_member,
                s.staff_name,
                SUM(s.hours_logged) as total_hours,
                SUM(s.billable_amount) as total_amount
            FROM `tabCA Timesheet Entry` s
            WHERE s.engagement = %s AND s.docstatus != 2
            GROUP BY s.staff_member, s.staff_name
            """,
            [self.name],
            as_dict=True,
        )
        return result

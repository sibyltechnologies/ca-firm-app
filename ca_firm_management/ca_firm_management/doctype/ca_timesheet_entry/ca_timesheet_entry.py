import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today


class CATimesheetEntry(Document):
    def before_save(self):
        self._calculate_billable_amount()
        self._validate_hours()

    def _calculate_billable_amount(self):
        if self.is_billable and self.hours_logged and self.staff_member:
            hourly_rate = frappe.db.get_value("CA Staff Profile", self.staff_member, "hourly_rate") or 0
            self.billable_amount = float(self.hours_logged) * float(hourly_rate)
        else:
            self.billable_amount = 0

    def _validate_hours(self):
        if not self.hours_logged or self.hours_logged <= 0:
            frappe.throw("Hours Logged must be greater than zero.")
        if self.hours_logged > 24:
            frappe.throw("Hours cannot exceed 24 in a single entry.")

        # Warn if total daily hours exceed 12
        existing = frappe.db.sql(
            """SELECT SUM(hours_logged) FROM `tabCA Timesheet Entry`
               WHERE staff_member = %s AND work_date = %s
               AND name != %s AND docstatus != 2""",
            [self.staff_member, self.work_date, self.name or ""],
        )
        total_today = (existing[0][0] or 0) + self.hours_logged
        if total_today > 12:
            frappe.msgprint(
                f"Total hours for {self.staff_name} on {self.work_date} will be {total_today}h. Please verify.",
                indicator="orange",
                alert=True,
            )

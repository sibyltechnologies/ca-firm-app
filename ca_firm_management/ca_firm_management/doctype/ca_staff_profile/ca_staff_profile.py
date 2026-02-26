import frappe
from frappe.model.document import Document
from frappe.utils import today, add_months, get_first_day, get_last_day


class CAStaffProfile(Document):
    def validate(self):
        if self.icap_membership_type in ("FCA", "ACA") and not self.icap_membership_no:
            frappe.msgprint(
                "ICAP Membership No. should be entered for qualified CAs.",
                indicator="yellow",
                alert=True,
            )

    def on_update(self):
        if self.user_account and self.role_in_firm:
            self._sync_user_role()

    def _sync_user_role(self):
        """Ensure the linked ERPNext user has the correct CA role"""
        user_doc = frappe.get_doc("User", self.user_account)
        existing_roles = [r.role for r in user_doc.roles]
        if self.role_in_firm not in existing_roles:
            user_doc.append("roles", {"role": self.role_in_firm})
            user_doc.save(ignore_permissions=True)
            frappe.msgprint(
                f"Role '{self.role_in_firm}' assigned to user {self.user_account}.",
                indicator="green",
                alert=True,
            )

    @frappe.whitelist()
    def get_utilization(self, month=None):
        """Return utilization stats for current or given month"""
        if not month:
            month = today()[:7]  # YYYY-MM
        month_start = get_first_day(month + "-01")
        month_end = get_last_day(month + "-01")

        result = frappe.db.sql(
            """
            SELECT 
                SUM(hours_logged) as total_hours,
                COUNT(DISTINCT engagement) as engagements_worked
            FROM `tabCA Timesheet Entry`
            WHERE staff_member = %s
              AND work_date BETWEEN %s AND %s
              AND docstatus != 2
            """,
            [self.name, month_start, month_end],
            as_dict=True,
        )
        total = result[0].total_hours or 0
        target = self.monthly_target_hours or 160
        utilization_pct = round((total / target) * 100, 1) if target else 0
        return {
            "month": month,
            "hours_logged": total,
            "target_hours": target,
            "utilization_percent": utilization_pct,
            "engagements_count": result[0].engagements_worked or 0,
        }

    @frappe.whitelist()
    def get_current_engagements(self):
        return frappe.get_all(
            "CA Engagement",
            filters={
                "engagement_partner": self.name,
                "status": ["in", ["Planning", "In Progress", "Under Review"]],
            },
            fields=["name", "client_name", "engagement_type", "deadline", "status", "progress_percent"],
            order_by="deadline asc",
        ) + frappe.get_all(
            "CA Engagement",
            filters={
                "engagement_manager": self.name,
                "status": ["in", ["Planning", "In Progress", "Under Review"]],
            },
            fields=["name", "client_name", "engagement_type", "deadline", "status", "progress_percent"],
            order_by="deadline asc",
        )

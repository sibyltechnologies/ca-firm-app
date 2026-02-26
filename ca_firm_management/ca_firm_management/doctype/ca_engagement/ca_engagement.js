frappe.ui.form.on("CA Engagement", {
    refresh(frm) {
        frm._setup_indicators(frm);
        frm._setup_buttons(frm);
        frm._setup_progress_bar(frm);
    },

    _setup_indicators(frm) {
        const statusColors = {
            Planning: "blue",
            "In Progress": "yellow",
            "Under Review": "orange",
            "Pending Client": "purple",
            Completed: "green",
            Billed: "teal",
            Cancelled: "red",
        };
        frm.dashboard.add_indicator(
            __("Status: {0}", [frm.doc.status]),
            statusColors[frm.doc.status] || "grey"
        );

        if (frm.doc.deadline) {
            frappe.call({
                method: "get_days_to_deadline",
                doc: frm.doc,
                callback(r) {
                    const days = r.message;
                    if (days !== null) {
                        const color = days < 0 ? "red" : days <= 7 ? "orange" : "green";
                        frm.dashboard.add_indicator(
                            days < 0
                                ? __("OVERDUE by {0} days", [Math.abs(days)])
                                : __("{0} days to deadline", [days]),
                            color
                        );
                    }
                },
            });
        }
    },

    _setup_buttons(frm) {
        if (frm.is_new()) return;

        if (!frm.doc.docstatus) {
            // Draft state
            frm.add_custom_button(__("Log Time"), () => {
                frappe.new_doc("CA Timesheet Entry", {
                    engagement: frm.doc.name,
                    client: frm.doc.client,
                    engagement_partner: frm.doc.engagement_partner,
                });
            }, __("Actions"));

            if (frm.doc.status === "In Progress" || frm.doc.status === "Under Review") {
                frm.add_custom_button(__("Mark Complete"), () => {
                    frappe.confirm(
                        __("Mark engagement as completed?"),
                        () => frappe.call({
                            method: "mark_complete",
                            doc: frm.doc,
                            callback() { frm.reload_doc(); },
                        })
                    );
                }, __("Actions"));
            }
        }

        if (frm.doc.docstatus === 1) {
            // Submitted — can raise invoice
            frm.add_custom_button(__("Create Invoice"), () => {
                frappe.new_doc("CA Invoice", {
                    client: frm.doc.client,
                    engagement: frm.doc.name,
                    amount: frm.doc.fee_amount,
                    engagement_type: frm.doc.engagement_type,
                });
            }, __("Actions"));
        }

        frm.add_custom_button(__("Time Summary"), () => {
            frappe.call({
                method: "get_timesheet_summary",
                doc: frm.doc,
                callback(r) {
                    const rows = (r.message || []).map(
                        (x) => `<tr><td>${x.staff_name}</td><td>${x.total_hours}h</td>
                                 <td>PKR ${frappe.utils.fmt_money(x.total_amount)}</td></tr>`
                    ).join("") || "<tr><td colspan='3'>No time logged yet.</td></tr>";
                    frappe.msgprint({
                        title: __("Time Summary"),
                        message: `<table class='table table-bordered'>
                            <thead><tr><th>Staff</th><th>Hours</th><th>Amount</th></tr></thead>
                            <tbody>${rows}</tbody>
                        </table>`,
                    });
                },
            });
        }, __("View"));
    },

    _setup_progress_bar(frm) {
        if (frm.doc.progress_percent !== undefined) {
            frm.dashboard.add_progress(__("Progress"), frm.doc.progress_percent);
        }
    },

    client(frm) {
        if (frm.doc.client) {
            frappe.db.get_value("CA Client", frm.doc.client, [
                "assigned_partner", "assigned_manager", "risk_rating"
            ], (r) => {
                if (r) {
                    frm.set_value("engagement_partner", r.assigned_partner);
                    frm.set_value("engagement_manager", r.assigned_manager);
                    if (r.risk_rating === "High" || r.risk_rating === "Very High") {
                        frappe.show_alert({
                            message: __("⚠️ High-risk client. Apply enhanced procedures."),
                            indicator: "orange",
                        });
                    }
                }
            });
        }
    },

    fee_type(frm) {
        if (frm.doc.fee_type === "Hourly Rate") {
            frm.set_df_property("fee_amount", "label", "Hourly Rate (PKR)");
            frm.set_df_property("fee_amount", "description", "Per hour rate; total computed from timesheets");
        } else {
            frm.set_df_property("fee_amount", "label", "Fee Amount (PKR)");
            frm.set_df_property("fee_amount", "description", "");
        }
    },
});

frappe.ui.form.on("CA Client", {
    refresh(frm) {
        frm.set_intro(
            frm.doc.status === "Blacklisted"
                ? __("⚠️ This client is blacklisted. Review before any new engagement.")
                : "",
            frm.doc.status === "Blacklisted" ? "red" : ""
        );

        // Risk badge color
        const riskColors = { Low: "green", Medium: "yellow", High: "orange", "Very High": "red" };
        if (frm.doc.risk_rating) {
            frm.dashboard.add_indicator(
                __("Risk: {0}", [frm.doc.risk_rating]),
                riskColors[frm.doc.risk_rating] || "grey"
            );
        }

        // Quick Action Buttons
        if (!frm.is_new()) {
            frm.add_custom_button(__("New Engagement"), () => {
                frappe.new_doc("CA Engagement", { client: frm.doc.name, client_name: frm.doc.client_name });
            }, __("Actions"));

            frm.add_custom_button(__("Log Contact"), () => {
                frappe.new_doc("CA Contact Log", { client: frm.doc.name });
            }, __("Actions"));

            frm.add_custom_button(__("View Engagements"), () => {
                frappe.route_options = { client: frm.doc.name };
                frappe.set_route("List", "CA Engagement");
            }, __("View"));

            frm.add_custom_button(__("View Invoices"), () => {
                frappe.route_options = { client: frm.doc.name };
                frappe.set_route("List", "CA Invoice");
            }, __("View"));
        }
    },

    entity_type(frm) {
        // Auto-suggest risk rating for high-risk entity types
        const highRiskTypes = ["Public Limited Company", "Foreign Branch"];
        if (highRiskTypes.includes(frm.doc.entity_type) && frm.doc.risk_rating === "Low") {
            frappe.show_alert({
                message: __("Consider reviewing risk rating for {0} entity types.", [frm.doc.entity_type]),
                indicator: "orange",
            });
        }
    },

    status(frm) {
        if (frm.doc.status === "Blacklisted") {
            frappe.msgprint({
                title: __("Blacklist Warning"),
                indicator: "red",
                message: __("This client is being blacklisted. All active engagements should be reviewed."),
            });
        }
    },
});

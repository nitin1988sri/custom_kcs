frappe.ui.form.on("Salary Structure", {
    onload: function(frm) {
        setTimeout(() => {
            if (frm.is_new() && frm.doc.company) {
                frm.set_value("company", "");
            }

            // Always show both on load
            frm.set_df_property("company", "hidden", 0);
            frm.set_df_property("customer", "hidden", 0);
        }, 200);
    },

    refresh: function(frm) {
        toggle_customer_company_fields(frm);
    },

    customer: function(frm) {
        toggle_customer_company_fields(frm);
    },

    company: function(frm) {
        toggle_customer_company_fields(frm);
    }
});

function toggle_customer_company_fields(frm) {
    if (frm.doc.customer) {
        // Customer selected: company = "test", hide company
        if (frm.doc.company !== "test") {
            frm.set_value("company", "Select compony");
        }
        frm.set_df_property("company", "hidden", 1);
        frm.set_df_property("customer", "hidden", 0);
    } else if (frm.doc.company) {
        // Company selected: hide customer
        frm.set_df_property("customer", "hidden", 1);
        frm.set_df_property("company", "hidden", 0);
    } else {
        // Nothing selected: show both
        frm.set_df_property("company", "hidden", 0);
        frm.set_df_property("customer", "hidden", 0);
    }
}

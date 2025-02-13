frappe.ui.form.on("Contract", {
    refresh: function(frm) {
        frm.fields_dict["roles"].grid.get_field("role").get_query = function() {
            return {};
        };
    }
});

frappe.ui.form.on("Contract Role", {
    role: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (frm.doc.branch && row.role) {
            fetchPersonnelCount(frm, cdt, cdn, row.role, frm.doc.branch);
        }
    },
    branch: function(frm) {
        frm.refresh_field("roles");  
    }
});

function fetchPersonnelCount(frm, cdt, cdn, role, branch) {
    frappe.call({
        method: "custom_kcs.src.contract.get_employee_count",
        args: {
            branch: branch,
            role: role
        },
        callback: function(response) {
            if (response.message) {
                frappe.model.set_value(cdt, cdn, "no_of_personnel", response.message);
            } else {
                frappe.msgprint("No employees found for this role in the selected branch.");
            }
        }
    });
}

frappe.ui.form.on('Employee', {
    client: function (frm) {
        if (frm.doc.client) {
            frappe.call({
                method: "custom_kcs.src.employee.get_branches_by_client",
                args: {
                    client: frm.doc.client
                },
                callback: function (response) {
                    let branches = response.message || [];
                    frm.set_query("branch", function () {
                        return {
                            filters: [["name", "in", branches]]
                        };
                    });
                }
            });
        }
    }
});

frappe.ui.form.on('Employee', {
    validate: function(frm) {
        let required_fields = ["company", "designation", "grade", "client", "branch", "shift", "department", "employment_type"];
        
        required_fields.forEach(field => {
            if (!frm.doc[field]) {
                frappe.throw(`${frappe.meta.get_docfield("Employee", field).label} is mandatory.`);
            }
        });
    }
});

frappe.ui.form.on('Employee', {
    setup: function(frm) {
        frm.set_query("contract", () => {
            return {
                query: "custom_kcs.src.employee.get_active_contracts",
                filters: {
                    client: frm.doc.client,
                    branch: frm.doc.branch
                }
            };
        });
    },
});
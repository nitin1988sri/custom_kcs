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
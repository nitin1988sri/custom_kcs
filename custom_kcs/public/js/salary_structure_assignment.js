frappe.ui.form.on('Salary Structure Assignment', {
    salary_structure: function(frm) {
        if (frm.doc.salary_structure) {
            frappe.call({
                method: "custom_kcs.src.salary_structure_assignment.get_salary_structure_details",
                args: {
                    salary_structure_name: frm.doc.salary_structure
                },
                callback: function(r) {
                    if (r.message) {
                        let in_hand_amount = r.message.in_hand || 0;
                        frm.set_value("base", in_hand_amount);
                    }
                }
            });
        }
    }
});

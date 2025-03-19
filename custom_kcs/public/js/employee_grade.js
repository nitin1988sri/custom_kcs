frappe.ui.form.on('Employee Grade', {
    default_salary_structure: function(frm) {
        if (frm.doc.default_salary_structure) {
            frappe.call({
                method: "custom_kcs.src.employee_grade.get_salary_structure_details",
                args: {
                    salary_structure_name: frm.doc.default_salary_structure
                },
                callback: function(r) {
                    if (r.message) {
                        let in_hand_amount = r.message.in_hand || 0;
                        frm.set_value("default_base_pay", in_hand_amount);
                    }
                }
            });
        }
    }
});

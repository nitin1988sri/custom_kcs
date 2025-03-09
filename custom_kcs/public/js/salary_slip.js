frappe.ui.form.on("Salary Slip", {
    employee: function (frm) {
        if (frm.doc.employee) {
            frappe.call({
                method: "custom_kcs.src.custom_salary_slip.get_employee_attendance_data",
                args: {
                    employee: frm.doc.employee,
                    start_date: frm.doc.start_date,
                    end_date: frm.doc.end_date
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_value("payment_days", r.message.payment_days);
                        frm.set_value("absent_days", r.message.absent_days);
                        frm.set_value("incentive_days", r.message.incentive_days);

                        frm.set_value("earnings", [
                            {
                                "salary_component": "In Hand",
                                "amount": r.message.in_hand_salary
                            },
                            {
                                "salary_component": "Incentive",
                                "amount": r.message.incentive_salary
                            }
                        ]);

                        frm.set_value("gross_pay", r.message.gross_pay);
                        frm.set_value("net_pay", r.message.rounded_gross_pay);
                        frm.set_value("total_in_words", r.message.total_in_words);
                        frm.refresh_field("payment_days");
                        frm.refresh_field("absent_days");
                        frm.refresh_field("incentive_days");
                        frm.refresh_field("earnings");
                        frm.refresh_field("gross_pay");
                        frm.refresh_field("rounded_total");
                        frm.refresh_field("net_pay");
                        frm.refresh_field("total_in_words");
                    }
                }
            });
        }
    }
});

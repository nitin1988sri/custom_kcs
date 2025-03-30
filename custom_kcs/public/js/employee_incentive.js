frappe.ui.form.on('Employee Incentive', {
    employee: function(frm) {
      trigger_incentive_fetch(frm);
    },
    payroll_date: function(frm) {
      trigger_incentive_fetch(frm);
    }
  });
  
  function trigger_incentive_fetch(frm) {
    if (frm.doc.employee && frm.doc.payroll_date) {
      let start_date = frappe.datetime.month_start(frm.doc.payroll_date);
  
      frappe.call({
        method: "custom_kcs.src.empolyee_incentive.calculate_incentive_for_employee",
        args: {
          employee: frm.doc.employee,
          start_date: start_date
        },
        callback: function(r) {
          if (r.message) {
            frm.set_value("incentive_amount", r.message.incentive_amount || 0);
            frm.set_value("incentive_days", r.message.incentive_days || 0);
            frm.refresh_field("incentive_amount");
            frm.refresh_field("incentive_days");
          }
        }
      });
    }
  }

  
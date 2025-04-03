frappe.ui.form.on('Payroll Entry', {
    refresh: function(frm) {
      frm.add_custom_button(__('Generate Employee Incentives'), () => {
  
        // 🔍 Check if Start Date is filled
        if (!frm.doc.start_date) {
          frappe.msgprint("⚠️ Please select Start Date first.");
          return;
        }
  
        // ✅ If Start Date exists, call the method with that date
        frappe.confirm(
          `Are you sure you want to generate Employee Incentives for <b>${frm.doc.start_date}</b>?`,
          () => {
            frappe.call({
              method: 'custom_kcs.src.cron.employee_Incentive.generate_employee_incentives_for_all',
              args: {
                start_date: frm.doc.start_date
              },
              callback: function(r) {
                if (r.message && r.message.status === "success") {
                  frappe.msgprint(`${r.message.total_created} Employee Incentives created.`);
                } else {
                  frappe.msgprint('⚠️ Something went wrong while generating incentives.');
                }
              }
            });
          }
        );
      }).addClass('btn-primary');
    }
  });
  
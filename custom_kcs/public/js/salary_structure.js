frappe.ui.form.on("Salary Structure", {
    onload: function(frm) {
        clear_fields_after_delay(frm);
    },

    refresh: function(frm) {
        clear_fields_after_delay(frm);
    },

});

function clear_fields_after_delay(frm) {
    if (frm.is_new()) {
        setTimeout(() => {
            frm.set_value("company", "");
            frm.set_value("customer", "");
        }, 300);  
    }
}

frappe.ui.form.on('Salary Structure', {
    customer: function(frm) {
      if (frm.doc.customer && frm.doc.customer !== "Null") {
        
        frm.set_value('company', 'Null');
  
      }
    },
    company: function(frm) {
        if (frm.doc.company && frm.doc.company !== "Null") {
          frm.set_value('customer', "");
            }
      }
  });
frappe.ui.form.on("Salary Structure", {
    validate: function(frm) {
        if (!frm.doc.company && !frm.doc.customer) {
            frappe.throw("Please select either Company or Customer.");
        }
    }
});
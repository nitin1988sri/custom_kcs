


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
    },
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
    validate: function(frm) {
        // Aadhaar Validation (12-digit)
        if (!/^\d{12}$/.test(frm.doc.aadhaar_number || '')) {
            frappe.throw("❌ Aadhaar Number must be a 12-digit number");
        }

        // ESIC Validation (10-digit)
        if (!/^\d{10}$/.test(frm.doc.esic_number || '')) {
            frappe.throw("❌ ESIC Number must be a 10-digit number");
        }

        // PAN Validation (ABCDE1234F format)
        if (!/^[A-Z]{5}[0-9]{4}[A-Z]{1}$/.test(frm.doc.pan_number || '')) {
            frappe.throw("❌ Invalid PAN Number format. Example: ABCDE1234F");
        }

        let required_fields = ["company", "designation", "grade", "client", "branch", "shift", "department", "employment_type"];
        
        required_fields.forEach(field => {
            if (!frm.doc[field]) {
                frappe.throw(`${frappe.meta.get_docfield("Employee", field).label} is mandatory.`);
            }
        });
    },
    naming_series: function (frm) {
        if (frm.doc.naming_series && frm.doc.naming_series.startsWith("HR-CONT")) {
            frm.set_value("employment_type", "Contract");
        }
    },

    onload: function (frm) {
        if (frm.doc.naming_series && frm.doc.naming_series.startsWith("HR-CONT")) {
            frm.set_value("employment_type", "Contract");
        }else{
            frm.set_value("employment_type", "");
        }
    },
    naming_series: function (frm) {
        if (frm.doc.naming_series && frm.doc.naming_series.startsWith("HR-CONT")) {
            frm.set_value("employment_type", "Contract");
        }
        else{
            frm.set_value("employment_type", "");
        }
    },

    onload: function (frm) {
        if (frm.doc.naming_series && frm.doc.naming_series.startsWith("HR-CONT")) {
            frm.set_value("employment_type", "Contract");
        }
    }
});
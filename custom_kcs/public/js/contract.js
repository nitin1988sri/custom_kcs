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


frappe.ui.form.on('Contract', {
	// Recalculate on form refresh
	refresh: function(frm) {
		calculateMonthlyContractValue(frm);
	},

	// Recalculate on validating the form
	validate: function(frm) {
		calculateMonthlyContractValue(frm);
	}
});

// Also, trigger calculation when any row in the child table "roles" is changed.
frappe.ui.form.on('Contract Role', {
	roles_add: function(frm, cdt, cdn) {
		calculateMonthlyContractValue(frm);
	},
	
	// When any field in the child table row changes
	no_of_personnel: function(frm, cdt, cdn) {
		calculateMonthlyContractValue(frm);
	},
	billing_rate: function(frm, cdt, cdn) {
		calculateMonthlyContractValue(frm);
	},
	
	// When a row is removed, recalc the total
	on_remove: function(frm, cdt, cdn) {
		calculateMonthlyContractValue(frm);
	}
});

function calculateMonthlyContractValue(frm) {
	let total = 0;
	
	(frm.doc.roles || []).forEach(function(row) {
		if (row.billing_rate && row.no_of_personnel) {
			total += row.billing_rate * row.no_of_personnel;
		}
	});
	
	frm.set_value("monthly_contract_value", total);
}

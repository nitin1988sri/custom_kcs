
frappe.ui.form.on('Contract Role', {
	roles_add: function(frm, cdt, cdn) {
		calculateMonthlyContractValue(frm);
	},
	
	no_of_personnel: function(frm, cdt, cdn) {
		calculateMonthlyContractValue(frm);
	},
	billing_rate: function(frm, cdt, cdn) {
		calculateMonthlyContractValue(frm);
	},
	
	on_remove: function(frm, cdt, cdn) {
		calculateMonthlyContractValue(frm);
	},
    form_render: function(frm, cdt, cdn) {
        setup_role_filters(frm);
    },
    role: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.role) {
            fetchPersonnelCount(frm, cdt, cdn, row.role, frm.doc.name);
        }
    },
    branch: function(frm) {
        frm.refresh_field("roles");  
    }
});

function calculateMonthlyContractValue(frm) {
	let total = 0;
	
	(frm.doc.roles || []).forEach(function(row) {
		if (row.billing_rate && row.no_of_personnel) {
			total += row.billing_rate * row.no_of_personnel;
		}
	});
	
}


frappe.ui.form.on("Branch", {
    onload: function(frm) {
        setup_role_filters(frm);
    },

    refresh: function(frm) {
        setup_role_filters(frm);

        console.log("Is New:", frm.doc.__islocal); 

        if (!frm.is_new()) {
            frm.add_custom_button("Get Employees", function () {
                frappe.call({
                    method: "custom_kcs.src.branch.fetch_employees_for_branch",
                    args: {
                        branch_name: frm.doc.name
                    },
                    callback: function (r) {
                        if (r.message) {
                            frappe.msgprint(r.message);
                            frm.reload_doc(); 
                        }
                    }
                });
            }).addClass("btn-primary");
        }
        frm.fields_dict["roles"].grid.get_field("role").get_query = function() {
            return {};
        };
    },
    party_name: function(frm) {
        frm.set_query("branch", function() {  
            return {
                filters: {
                    "client": frm.doc.client 
                }
            };
        });
    },
    // refresh: function(frm) {
        
    // }
});

function setup_role_filters(frm) {
    frm.fields_dict["roles"].grid.get_field("salary_structure").get_query = function(doc, cdt, cdn) {
        return {
            filters: [
                ["customer", "=", ""],
            ]
        };
    };

    frm.fields_dict["roles"].grid.get_field("contract_cost_structure").get_query = function(doc, cdt, cdn) {
        return {
            filters: [
                ["customer", "=", frm.doc.client],
            ]
        };
    };
}

function fetchPersonnelCount(frm, cdt, cdn, role, branch) {
    frappe.call({
        method: "custom_kcs.src.branch.get_employee_count",
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

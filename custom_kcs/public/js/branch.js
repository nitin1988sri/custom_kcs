frappe.ui.form.on("Branch", {
    refresh: function(frm) {
        frm.fields_dict["roles"].grid.get_field("role").get_query = function() {
            return {};
        };
    }
});

frappe.ui.form.on("Contract Role", {
    role: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.role) {
            fetchPersonnelCount(frm, cdt, cdn, row.role, frm.doc.client);
        }
    },
    branch: function(frm) {
        frm.refresh_field("roles");  
    }
});

function fetchPersonnelCount(frm, cdt, cdn, role, client) {
    frappe.call({
        method: "custom_kcs.src.branch.get_employee_count",
        args: {
            client: client,
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
	refresh: function(frm) {
		calculateMonthlyContractValue(frm);
	},

	validate: function(frm) {
		calculateMonthlyContractValue(frm);
	}
});

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
	}
});

function calculateMonthlyContractValue(frm) {
	let total = 0;
	
	(frm.doc.roles || []).forEach(function(row) {
		if (row.billing_rate && row.no_of_personnel) {
			total += row.billing_rate * row.no_of_personnel;
		}
	});
	
	//frm.set_value("monthly_contract_value", total);
}

frappe.ui.form.on('Branch', {
    party_name: function(frm) {
        frm.set_query("branch", function() {  
            return {
                filters: {
                    "client": frm.doc.client 
                }
            };
        });
    }
});

frappe.ui.form.on('Contract', {
    party_name: function(frm) {
        if (frm.doc.party_name) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Contract",
                    fields: ["name"]
                },
                callback: function(response) {
                    let random_string = Math.random().toString(36).substring(2, 6).toUpperCase(); 
                    let contract_code = frm.doc.party_name + "-" + random_string;

                    frm.set_value("contract_code", contract_code);
                }
            });
        }
    }
});


frappe.ui.form.on('Branch', {
    client: function(frm) {
        frm.trigger("fetch_employees");
    },
    fetch_employees: function(frm) {
        if (!frm.doc.client) return;

        frappe.call({
            method: "custom_kcs.src.branch.get_employees_for_branch",
            args: {
                client: frm.doc.client,
            },
            callback: function(r) {
                if (r.message) {
                    frm.clear_table("employees_list");
                    r.message.forEach(emp => {
                        let row = frm.add_child("employees_list");
                        row.employee = emp.name;
                        row.employee_name = emp.employee_name;
                        row.designation = emp.designation;
                        row.shift = emp.shift;
                        row.branch = emp.branch;
                        row.date_of_joining = emp.date_of_joining;
                    });
                    frm.refresh_field("employees_list");
                }
            }
        });
    }
});


frappe.ui.form.on("Branch", {
    onload: function(frm) {
        setup_role_filters(frm);
    },

    refresh: function(frm) {
        setup_role_filters(frm);
    }
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

frappe.ui.form.on("Contract Role", {
    form_render: function(frm, cdt, cdn) {
        setup_role_filters(frm);
    }
})
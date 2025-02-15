document.addEventListener("DOMContentLoaded", function() {
    fetchEmployees();
    fetchBranches();
});

function fetchEmployees() {
    frappe.call({
        method: "custom_kcs.src.assign_temporary_transfer.get_employees",
        callback: function(response) {
            let employeeSelect = document.getElementById("employee");
            employeeSelect.innerHTML = "";
            response.message.forEach(emp => {
                let option = document.createElement("option");
                option.value = emp.name;
                option.text = emp.employee_name+" {"+ emp.branch+"}";
                employeeSelect.appendChild(option);
            });
        }
    });
}

function fetchBranches() {
    frappe.call({
        method: "custom_kcs.src.assign_temporary_transfer.get_branches",
        callback: function(response) {
            let branchSelect = document.getElementById("temp_branch");
            branchSelect.innerHTML = "";
            response.message.forEach(branch => {
                let option = document.createElement("option");
                option.value = branch.branch;
                option.text = branch.branch;
                branchSelect.appendChild(option);
            });
        }
    });
}

function transferSecurityGuard() {
    let employee_id = document.getElementById("employee").value;
    let temp_branch_id = document.getElementById("temp_branch").value;
    let start_date = document.getElementById("start_date").value;
    let end_date = document.getElementById("end_date").value;

    frappe.call({
        method: "custom_kcs.src.assign_temporary_transfer.assign_temporary_transfer",
        args: { employee_id, temp_branch_id, start_date, end_date },
        callback: function(response) {
            console.log(response)
            document.getElementById("response").innerHTML = `<p>${response.message}</p>`;
        }
    });
}


frappe.ready(function () {
    frappe.call({
        method: "custom_kcs.src.assign_temporary_transfer.validate_admin_access",
        callback: function (response) {
            if (!response.message) {  
                frappe.msgprint(__("You are not authorized to access this page."));
                window.location.href = "/app"; 
            }
        }
    });
});

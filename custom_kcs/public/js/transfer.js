document.addEventListener("DOMContentLoaded", function() {
    fetchEmployees();
    fetchBranches();

    setupEmployeeSearch();
});

function fetchEmployees() {
    frappe.call({
      method: "custom_kcs.src.assign_temporary_transfer.get_employees",
      callback: function(response) {
        employees_list = response.message;
        console.log(employees_list)
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

function setupEmployeeSearch() {
    const employeeInput = document.getElementById("employee_input");
    if (!employeeInput) {
        console.error("Element with ID 'employee_input' not found. Please ensure it exists in your HTML.");
        return;
    }
    
    const suggestionsContainer = document.getElementById("employee_suggestions");

    employeeInput.addEventListener("input", function(e) {
        let query = e.target.value.toLowerCase();
        suggestionsContainer.innerHTML = "";

        if (query.length === 0) {
            return; 
        }

        let filteredEmployees = employees_list.filter(emp => {
            return (
                emp.name.toLowerCase().includes(query) ||
                emp.employee_name.toLowerCase().includes(query)
            );
        });

        filteredEmployees.forEach(emp => {
            let suggestionItem = document.createElement("div");
            suggestionItem.className = "suggestion-item";
            
            suggestionItem.textContent = emp.name + "-" + emp.employee_name + (emp.shift_info || "");
            suggestionItem.setAttribute("data-emp-id", emp.name);

            suggestionItem.addEventListener("click", function() {
                employeeInput.value = this.textContent;
                employeeInput.setAttribute("data-selected-emp", this.getAttribute("data-emp-id"));
                suggestionsContainer.innerHTML = "";
            });
            suggestionsContainer.appendChild(suggestionItem);
        });
    });

    document.addEventListener("click", function(e) {
        if (!employeeInput.contains(e.target)) {
            suggestionsContainer.innerHTML = "";
        }
    });
}

function transferSecurityGuard() {
  let employeeInput = document.getElementById("employee_input");
  let employee_id = employeeInput.getAttribute("data-selected-emp");

  if (!employee_id) {
    frappe.msgprint("Please select a valid employee from the suggestions.");
    return;
  }

  let temp_branch_id = document.getElementById("temp_branch").value;
  let start_date = document.getElementById("start_date").value;
  let end_date = document.getElementById("end_date").value;

  frappe.call({
    method: "custom_kcs.src.assign_temporary_transfer.assign_temporary_transfer",
    args: { employee_id, temp_branch_id, start_date, end_date },
    callback: function(response) {
      console.log(response);
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

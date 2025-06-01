document.addEventListener("DOMContentLoaded", function() {
    fetchEmployees();
    fetchBranches();
    setupEmployeeSearch();
    fetchShiftTypes();
});

function fetchEmployees() {
    frappe.call({
      method: "custom_kcs.src.overtime.get_employees",
      callback: function(response) {
        employees_list = response.message;
      }
    });
  }

  function fetchShiftTypes() {
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Shift Type",
            fields: ["name"]
        },
        callback: function(response) {
            let shiftSelect = document.getElementById("overtime_shift");
            response.message.forEach(shift => {
                let option = document.createElement("option");
                option.value = shift.name;
                option.text = shift.name;
                shiftSelect.appendChild(option);
            });
        }
    });
}
function fetchBranches() {
    frappe.call({
        method: "custom_kcs.src.overtime.get_branches",
        callback: function(response) {
            let branchSelect = document.getElementById("overtime_branch");
            branchSelect.innerHTML = "";
            response.message.forEach(branch => {
                let option = document.createElement("option");
                option.value = branch.branch_name;
                option.text = branch.branch_name;
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

    // Move this inside the loop 👇
    suggestionItem.addEventListener("click", function() {
        employeeInput.value = this.textContent;
        employeeInput.setAttribute("data-selected-emp", this.getAttribute("data-emp-id"));
        suggestionsContainer.innerHTML = "";

        let emp_id = this.getAttribute("data-emp-id");

        // Fetch Last 2 Shifts
        frappe.call({
            method: "custom_kcs.src.overtime.get_last_two_shifts",
            args: { employee_id: emp_id },
            callback: function(res) {
                let shifts = res.message;
                let shiftInfoDiv = document.getElementById("shift_info");
                shiftInfoDiv.innerHTML = "";

                if (shifts.length > 0) {
                    shifts.forEach(shift => {
                        shiftInfoDiv.innerHTML += `<p>${shift.shift_type} at ${shift.branch} ( ${shift.check_in_time} )</p>`;
                    });
                }

                // Validation
                if (shifts.length >= 2) {
                    frappe.msgprint("Can't assign more than 2 shifts continuously.");
                    document.querySelector('.btn-primary').disabled = true;
                } else {
                    document.querySelector('.btn-primary').disabled = false;
                }
            }
        });
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

function create_overtime() {
    let employeeInput = document.getElementById("employee_input");
    let employee_id = employeeInput.getAttribute("data-selected-emp");

    if (!employee_id) {
        frappe.msgprint("Please select a valid employee from the suggestions.");
        return;
    }

    let overtime_branch = document.getElementById("overtime_branch").value;
    let overtime_shift = document.getElementById("overtime_shift").value;
    let start_date = document.getElementById("start_date").value;
    let end_date = document.getElementById("start_date").value;

    if (!overtime_shift) {
        frappe.msgprint("Please select an Overtime Shift.");
        return;
    }

    frappe.call({
        method: "custom_kcs.src.overtime.create_overtime",
        args: { employee_id, overtime_branch, start_date, end_date, overtime_shift },
        callback: function(response) {
            document.getElementById("response").innerHTML = `<p>${response.message}</p>`;
        }
    });
}


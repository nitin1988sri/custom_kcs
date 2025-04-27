function showLoader() {
    document.getElementById('loader').style.display = 'block';
}
function hideLoader() {
    document.getElementById('loader').style.display = 'none';
}
let shiftOptionsGlobal = '';
let statusOptions = '';
document.addEventListener('DOMContentLoaded', function() {


showLoader();

Promise.all([
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'Attendance Status',
            filters: { is_active: 1 },
            fields: ['status_name', 'is_default']
        }
    }),

    frappe.call({
        method: 'custom_kcs.src.employee_attendance.get_branches_for_manager',
        callback: function(res) {
            let branchFilter = document.getElementById('branch_filter');
            branchFilter.innerHTML = `<option value="">All Branches</option>`;  // Default option

            res.message.forEach(branch => {
                branchFilter.innerHTML += `<option value="${branch}">${branch}</option>`;
        });
    }
    }),
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'Shift Type',
            fields: ['name']
        }
    }),
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'Branch',
            fields: ['name']
        }
    })
]).then(res => {
    const status_res = res[0].message;
    const shift_res = res[1].message;

    if (status_res.length) {
        status_res.forEach(st => {
            statusOptions += `<option value="${st.status_name}" ${st.is_default ? 'selected' : ''}>${st.status_name}</option>`;
        });
    } else {
        document.getElementById('employee_table_container').innerHTML = `<div class="alert alert-warning text-center">No Attendance Status Found!</div>`;
        hideLoader();
        return;
    }
    if (shift_res.length) {
        shift_res.forEach(shift => {
            shiftOptionsGlobal += `<option value="${shift.name}">${shift.name}</option>`;
        });
    } else {
        document.getElementById('employee_table_container').innerHTML = `<div class="alert alert-warning text-center">No Shift Types Defined!</div>`;
        hideLoader();
        return;
    }
    loadEmployees();
    hideLoader();
    });

   
});

function loadEmployees() {
    let selectedBranch = document.getElementById('branch_filter').value;

    frappe.call({
        method: 'custom_kcs.src.employee_attendance.get_employees_for_bulk_attendance',
        args: { branch: selectedBranch }, 
        callback: function(r) {
            console.log(r);
            let employees = r.message;
            let html = `<table class="table">
                <thead>
                    <tr>
                        <th><input type="checkbox" id="select_all" /></th>
                        <th>Employee</th>
                        <th>Branch</th>
                        <th>Shift</th>
                        <th>Status</th>
                    </tr>
                </thead><tbody>`;

                if (!Array.isArray(employees) || employees.length === 0) {
                    document.getElementById('employee_table_container').innerHTML = `<div class="alert text-center">${employees.error}</div>`;
                    document.getElementById('mark_btn_container').innerHTML = ""; 
                    hideLoader();
                    return;
                }
                
                document.getElementById('mark_btn_container').innerHTML = `
                <button class="btn btn-primary" onclick="markBulkAttendance()">Mark Attendance</button>`;

                employees.forEach(emp => {

                let shiftOptions = shiftOptionsGlobal.replace(`value="${emp.shift}"`, `value="${emp.shift}" selected`);

                html += `<tr>
                    <td><input type="checkbox" class="emp-check" value="${emp.name}" checked></td>
                    <td>${emp.employee_name} (${emp.name})</td>
                    <td>
                            ${emp.branch}
                    </td>
                    <td>
                        <select id="shift_${emp.name}">
                            ${shiftOptions}
                        </select>
                    </td>
                    <td>
                        <select id="status_${emp.name}">
                            ${statusOptions}
                        </select>
                    </td>
                </tr>`;
            });

            html += `</tbody></table>`;
            document.getElementById('employee_table_container').innerHTML = html;

            document.getElementById('select_all').addEventListener('change', function() {
                document.querySelectorAll('.emp-check').forEach(cb => cb.checked = this.checked);
            });
        }
    });
}


function markBulkAttendance() {
    let successCount = 0;

    let selected = [];
    document.querySelectorAll('.emp-check:checked').forEach(box => {
        let emp_id = box.value;
        selected.push({
            employee: emp_id,
            branch: document.getElementById(`branch_${emp_id}`).value,
            shift_type: document.getElementById(`shift_${emp_id}`).value,
            status: document.getElementById(`status_${emp_id}`).value,
            work_location: document.getElementById(`branch_${emp_id}`).value
        });
    });

    selected.forEach(emp => {
        frappe.call({
            method: 'custom_kcs.src.employee_attendance.attendance',
            args: emp,
            callback: function(res) {
                successCount++;
                console.log(`Attendance marked for ${emp.employee}: ${res.message}`);
                if (successCount === selected.length) {
                    frappe.msgprint("✅ Bulk Attendance Marked Successfully!");
                }
            }
        });
    });

    document.getElementById('response').innerText = "Attendance marking initiated!";
}





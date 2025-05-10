

let statusOptions = '';


document.addEventListener("DOMContentLoaded", () => {
    loadBranches();
    loadShiftTypes(); 
    loadOvertimeEmployees();
});

function loadBranches() {
    frappe.call({
        method: 'custom_kcs.src.employee_attendance.get_branches_for_manager',
        callback: function(res) {
            let branchFilter = document.getElementById('branch_filter');
            branchFilter.innerHTML = `<option value="">All Branches</option>`;  // Default option

            res.message.forEach(branch => {
                branchFilter.innerHTML += `<option value="${branch}">${branch}</option>`;
        });
    }
    });
}

function loadShiftTypes() {
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'Shift Type',
            fields: ['name']
        },
        callback: function(res) {
            const shiftFilter = document.getElementById("shift_filter");
            shiftFilter.innerHTML = `<option value="">All Shifts</option>`;
            res.message.forEach(shift => {
                shiftFilter.innerHTML += `<option value="${shift.name}">${shift.name}</option>`;
            });
        }
    });
}


function loadStatus() {
frappe.call({
    method: 'frappe.client.get_list',
    args: {
        doctype: 'Attendance Status',
        filters: { is_active: 1 },
        fields: ['status_name', 'is_default']
    },
    callback: function(res) {
        res.message.forEach(st => {
            statusOptions += `<option value="${st.status_name}" ${st.is_default ? 'selected' : ''}>${st.status_name}</option>`;
        });
    }
});
}

function loadOvertimeEmployees() {
    loadStatus()
    const branch = document.getElementById("branch_filter").value;
    const shift_type = document.getElementById("shift_filter").value;

    frappe.call({
        method: "custom_kcs.src.overtime.get_overtime_employees_for_branch",
        args: { branch, shift_type },
        callback: (res) => {
            const container = document.getElementById("overtime_employee_container");
            let data = res.message;

            if (!data.length) {
                container.innerHTML = `<div class="alert alert-warning text-center">No overtime employees found.</div>`;
                return;
            }

            let html = `<table class="table"><thead>
                <tr><th><input type="checkbox" id="select_all" /></th><th>Employee</th><th>Overtime branch</th><th>Shift</th><th>Start date</th><th>End Date</th><th>Status</th></tr>
                </thead><tbody>`;

            data.forEach(emp => {
                html += `<tr>
                    <td><input type="checkbox" class="emp-check" value="${emp.employee}" checked></td>
                    <td>${emp.employee_name} (${emp.employee})</td>
                    <td id="overtime_branch_${emp.employee}">${emp.overtime_branch}</td>
                    <td id="shift_type_${emp.employee}">${emp.shift_type}</td>
                    <td id="start_date_${emp.employee}">${emp.start_date}</td>
                    <td>${emp.end_date}</td>
                    <td>
                         <select id="status_${emp.employee}" class="form-control">
                             ${statusOptions}
                         </select>
                    </td>
                </tr>`;
            });

            html += `</tbody></table>`;
            container.innerHTML = html;

            document.getElementById('select_all').addEventListener('change', function () {
                document.querySelectorAll('.emp-check').forEach(cb => cb.checked = this.checked);
            });
        }
    });
}

function submitOvertimeAttendance() {
    const selected = [];
    document.querySelectorAll('.emp-check:checked').forEach(box => {
        const emp = box.value;
        selected.push({
            employee: emp,
            status: document.getElementById(`status_${emp}`).value,
            branch: document.getElementById(`overtime_branch_${emp}`).innerText,
            shift_type: document.getElementById(`shift_type_${emp}`).innerText,
            attendance_date: document.getElementById(`start_date_${emp}`).innerText

        });
    });

    frappe.call({
        method: "custom_kcs.src.employee_attendance.bulk_attendance",
        args: { data: JSON.stringify(selected) },
        callback: function (res) {
            document.getElementById("response").innerText = "Attendance submitted.";
        }
    });
}

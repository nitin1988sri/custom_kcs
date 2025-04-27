import frappe
from frappe.utils import nowdate
from frappe.utils import add_days, today


@frappe.whitelist()
def validate_admin_access():
    return "Administrator" in frappe.get_roles(frappe.session.user)

@frappe.whitelist()
def get_employees():
    employees = frappe.get_all("Employee", fields=["name", "employee_name", "branch"])
    
    for emp in employees:
        shift_logs = frappe.get_all(
            "Shift Log", 
            filters={"employee": emp.name}, 
            fields=["shift_type", "check_in_time", "branch"],
            order_by="check_in_time desc",
            limit_page_length=2
        )

        shift_info = ""
        for log in shift_logs:
            if log.shift_type and log.branch:
                shift_label = log.shift_type.lower()
                if shift_label == "day shift":
                    shift_info += f" (Day shift Branch:- {log.branch})"
                elif shift_label == "night shift":
                    shift_info += f" (Night shift Branch:- {log.branch})"
                else:
                    shift_info += f" ({shift_label.title()} Branch:- {log.branch})"
        
        emp["shift_info"] = shift_info

    return employees

@frappe.whitelist()
def get_branches():
    branches = frappe.get_all("Branch", fields=["branch"])
    return branches

@frappe.whitelist()
def create_overtime(employee_id, overtime_branch, start_date, end_date, overtime_shift):
    # if "Administrator" not in frappe.get_roles(frappe.session.user):
    #     frappe.throw("You are not authorized to perform this action.", frappe.PermissionError)

    employee = frappe.get_doc("Employee", employee_id)
    original_branch = employee.branch
    #current_contract = frappe.get_value("Contract", {"party_name": employee.client}, "name")

    # if not current_contract:
    #     frappe.throw("No active contract found for this employee!")

    # new_contract = frappe.get_value("Contract", {"branch": temp_branch_id}, "name")
    # if not new_contract:
    #     frappe.throw("No active contract found for this branch!")

    # new_rate = None
    # contract_roles = frappe.get_all( "Contract Role", filters={"parent": new_contract},fields=["role", "billing_rate"])
    # for role in contract_roles:
    #     if role['role'] == employee.designation:
    #         new_rate = role['billing_rate']
    #         break

    # if not new_rate:
    #     frappe.throw("No matching role found in the new contract!")

    validate_overtime_assignment(employee_id, start_date, overtime_shift)

    temp_transfer = frappe.get_doc({
        "doctype": "Overtime",
        "employee": employee_id,
        "original_branch": original_branch,
        "overtime_branch": overtime_branch,
        "start_date": start_date,
        "end_date": end_date,
        "shift_type": overtime_shift,
        "status": "Active"
    })
    temp_transfer.insert()
    frappe.db.commit()

    return f"Employee {employee.name} has been allocated for overtime to {overtime_branch} from {start_date} to {end_date}."


def validate_overtime_assignment(employee, date, shift_type):
    existing = frappe.get_all(
        "Overtime",
        filters={
            "employee": employee,
            "start_date": ["<=", date],
            "end_date": [">=", date],
            "shift_type": shift_type,
            "status": "Active"
        },
        fields=["name", "overtime_branch"]
    )
    if existing:
        return f"This employee is already allocated to {existing[0].overtime_branch} for {shift_type} shift on {date}."
    return "✅ No conflict, you can assign."


@frappe.whitelist()
def get_last_two_shifts(employee_id):
    yesterday = add_days(today(), -1)
    shifts = frappe.get_all(
        "Shift Log",
        filters={
            "employee": employee_id,
            "check_in_time": yesterday
        },
        fields=["shift_type", "branch", "check_in_time"],
        order_by="check_in_time desc"
    )

    if len(shifts) >= 2:
        return {
            "error": "❌ This employee already completed 2 shifts on {}".format(yesterday),
            "shifts": shifts
        }

    return {
        "shifts": shifts
    }

@frappe.whitelist()
def get_overtime_employees_for_branch(branch=None):
    if not branch:
        branches = get_branches_for_manager()
        if not branches:
            return []
    else:
        branches = [branch]

    placeholders = ','.join(['%s'] * len(branches))

    query = f"""
        SELECT 
            ot.employee,
            e.employee_name,
            ot.overtime_branch,
            ot.shift_type,
            ot.start_date,
            ot.end_date
        FROM `tabOvertime` ot
        LEFT JOIN `tabEmployee` e ON ot.employee = e.name
        WHERE ot.status = 'Active'
        AND ot.overtime_branch IN ({placeholders})
        AND NOT EXISTS (
            SELECT 1 FROM `tabAttendance` att
            WHERE att.employee = ot.employee
            AND att.attendance_date BETWEEN ot.start_date AND ot.end_date
        )
    """

    params = branches

    overtime_employees = frappe.db.sql(query, params, as_dict=True)

    return overtime_employees



@frappe.whitelist()
def get_branches_for_manager():
    user = frappe.session.user
    employee_id = frappe.db.get_value("Employee", {"user_id": user}, "name")

    if not employee_id:
        return []

    branches = frappe.get_all(
        "Branch",
        filters={"branch_manager": employee_id},
        pluck="name"
    )

    return branches
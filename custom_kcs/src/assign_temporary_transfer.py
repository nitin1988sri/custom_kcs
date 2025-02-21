import frappe
from frappe.utils import nowdate


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
            fields=["shift_type", "check_in_time"],
            order_by="check_in_time desc",
            limit_page_length=2
        )
        shift_info = ""
        for log in shift_logs:
            if log.shift_type.lower() == "day shift":
                shift_info += " (Day shift done)"
            elif log.shift_type.lower() == "night shift":
                shift_info += " (Night shift done)"
        emp["shift_info"] = shift_info
    return employees

@frappe.whitelist()
def get_branches():
    branches = frappe.get_all("Branch", fields=["branch"])
    return branches

@frappe.whitelist()
def assign_temporary_transfer(employee_id, temp_branch_id, start_date, end_date):
    if "Administrator" not in frappe.get_roles(frappe.session.user):
        frappe.throw("You are not authorized to perform this action.", frappe.PermissionError)

    employee = frappe.get_doc("Employee", employee_id)
    original_branch = employee.branch
    current_contract = frappe.get_value("Contract", {"party_name": employee.client}, "name")

    if not current_contract:
        frappe.throw("No active contract found for this employee!")

    new_contract = frappe.get_value("Contract", {"branch": temp_branch_id}, "name")
    if not new_contract:
        frappe.throw("No active contract found for this branch!")

    new_rate = None
    contract_roles = frappe.get_all( "Contract Role", filters={"parent": new_contract},fields=["role", "billing_rate"])
    for role in contract_roles:
        if role['role'] == employee.designation:
            new_rate = role['billing_rate']
            break

    if not new_rate:
        frappe.throw("No matching role found in the new contract!")

    temp_transfer = frappe.get_doc({
        "doctype": "Temporary Transfer",
        "employee": employee_id,
        "original_branch": original_branch,
        "temporary_branch": temp_branch_id,
        "start_date": start_date,
        "end_date": end_date,
        "billing_rate": new_rate,
        "transfer_status": "Active"
    })
    temp_transfer.insert()
    frappe.db.commit()

    return f"Employee {employee.name} has been temporarily transferred to {temp_branch_id} from {start_date} to {end_date}."


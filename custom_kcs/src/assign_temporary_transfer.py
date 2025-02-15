import frappe
from frappe.utils import nowdate

@frappe.whitelist()
def get_employees():
    employees = frappe.get_all("Employee", fields=["name", "employee_name"])
    return employees

@frappe.whitelist()
def get_branches():
    branches = frappe.get_all("Branch", fields=["branch"])
    return branches

@frappe.whitelist()
def assign_temporary_transfer(employee_id, temp_branch_id, start_date, end_date):
    employee = frappe.get_doc("Employee", employee_id)

    original_branch = employee.branch
    current_contract = frappe.get_value("Contract", {"party_name": employee.client}, "name")
    
    if not current_contract:
        frappe.throw("No active contract found for this employee!")

    new_contract = frappe.get_value("Contract", {"branch": temp_branch_id}, "name")
    if not new_contract:
        frappe.throw("No active contract found for this branch!")

    new_rate = None
    contract_doc = frappe.get_doc("Contract", new_contract)
    for role in contract_doc.get("roles"):
        if role.role == employee.role:
            new_rate = role.billing_rate
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
        "billing_rate_at_temporary_branch": new_rate,
        "transfer_status": "Active"
    })
    temp_transfer.insert()
    frappe.db.commit()

    return f"Employee {employee.name} has been temporarily transferred to {temp_branch_id} from {start_date} to {end_date}."


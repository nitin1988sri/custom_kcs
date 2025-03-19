import frappe
import random
import string

def update_personnel_count(doc, method):
    frappe.logger().info(f"Updating contract: {doc.name}")
    if not doc.roles:
        frappe.logger().error(f"No roles found in contract: {doc.name}")

    for role in doc.roles:
        frappe.logger().info(f"Processing role: {role.role}")
        role.no_of_personnel = frappe.db.count(
            "Employee",
            filters={
                "designation": role.role, 
                "branch": doc.branch
            }
        )

@frappe.whitelist()
def get_employee_count(role):
    count = frappe.db.count("Employee", filters={"designation": role})
    return count


@frappe.whitelist()
def generate_contract_code(party_name):
    """Generate unique contract code with Party Name and random string."""
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))  
    contract_code = f"{party_name}-{random_string}"

    while frappe.db.exists("Contract", {"contract_code": contract_code}):
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        contract_code = f"{party_name}-{random_string}"

    return contract_code

def before_insert(doc, method):
    if not doc.contract_code:
        doc.contract_code = generate_contract_code(doc.party_name)

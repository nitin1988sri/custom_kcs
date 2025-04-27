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

@frappe.whitelist()
def get_employees_for_contract(client, branch):
    return frappe.get_all("Employee",
        filters={
            "client": client,
            "branch": branch,
            "status": "Active"
        },
        fields=["name", "employee_name", "designation", "branch","shift", "date_of_joining"]
    )


def on_contract_submit(doc, method):
    for row in doc.contract_branches:
        frappe.db.set_value("Branch", row.branch, "linked_contract", doc.name)

def clear_linked_contract(doc, method):
    for row in doc.contract_branches:
        frappe.db.set_value("Branch", row.branch, "linked_contract", "")

def update_mega_contract_links(doc, method):
    if doc.mega_contract:
        mega = frappe.get_doc("Mega Contract", doc.mega_contract)
        
        already = [d.contract for d in mega.get("linked_contracts")]

        if doc.name not in already:
            row = mega.append("linked_contracts", {})
            row.contract = doc.name 
            mega.save(ignore_permissions=True)
            frappe.msgprint(f"✅ Contract '{doc.name}' linked to Mega Contract '{doc.mega_contract}'")


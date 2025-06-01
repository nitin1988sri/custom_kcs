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
def get_employee_count(role, branch):
    count = frappe.db.count("Employee", filters={"branch":branch, "designation": role})
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

@frappe.whitelist()
def get_employees_for_branch(client):
    return frappe.get_all("Employee",
        filters={
            "client": client,
            "status": "Active"
        },
        fields=["name", "employee_name", "designation", "branch","shift", "date_of_joining"]
    )

@frappe.whitelist()
def fetch_employees_for_branch(branch_name):
    branch_doc = frappe.get_doc("Branch", branch_name)

    # Clear old employees
    branch_doc.set("employees_list", [])

    employees = frappe.get_all("Employee", 
        filters={
            "branch": branch_doc.name,
            "client": branch_doc.client  # assuming you have this Link field
        },
        fields=["name", "employee_name", "designation", "shift", "branch", "date_of_joining"]
    )

    for emp in employees:
        branch_doc.append("employees_list", {
            "employee": emp.name,
            "employee_name": emp.employee_name,
            "designation": emp.designation,
            "shift": emp.shift,
            "branch": emp.branch,
            "date_of_joining": emp.date_of_joining
        })
    branch_doc.save()
    return f"{len(employees)} employee(s) added to Employees List"

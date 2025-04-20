
import frappe
from frappe import _

def create(doc, method):

    if doc.is_client_slip:
        return

    branch = doc.branch
    employee = doc.employee
    role = doc.designation  # assuming designation == Role

    # Step 1: Get contract role child table from Branch
    contract_roles = frappe.get_all("Contract Role",
        filters={
            "parent": branch,
            "parenttype": "Branch",
            "role": role
        },
        fields=["client_cost_structure"]
    )

    if not contract_roles or not contract_roles[0].get("client_cost_structure"):
        frappe.throw(f"❌ No client structure found for role: {role} in branch {branch}")
        return

    client_structure = contract_roles[0]["client_cost_structure"]
    
    # Step 2: Prevent duplicate creation
    exists = frappe.db.exists("Salary Slip", {
        "employee": employee,
        "start_date": doc.start_date,
        "end_date": doc.end_date,
        "is_client_slip": 1
    })

    if exists:
        return

    # Step 3: Create client-side salary slip
    client_doc = frappe.new_doc("Salary Slip")
    client_doc.employee = employee
    client_doc.salary_structure = client_structure
    client_doc.start_date = doc.start_date
    client_doc.end_date = doc.end_date
    client_doc.payroll_entry = doc.payroll_entry
    client_doc.branch = doc.branch
    client_doc.company = doc.company
    client_doc.posting_date = doc.posting_date
    client_doc.payroll_frequency = doc.payroll_frequency
    client_doc.is_client_slip = 1
    client_doc.reference_salary_slip = doc.name
    client_doc.save()
    client_doc.submit()

    frappe.logger().info(f"✅ Client Salary Slip Created Using Structure: {client_structure}")

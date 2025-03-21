import frappe

@frappe.whitelist()
def get_branches_by_client(client):
    if not client:
        return []

    branches = frappe.get_all("Branch", filters={"client": client}, pluck="name")
    return branches

def validate_employee(doc, method):
    required_fields = ["company", "designation", "grade", "client", "branch", "shift", "department", "employment_type"]
    
    for field in required_fields:
        if not doc.get(field):
            frappe.throw(f"{frappe.get_meta('Employee').get_label(field)} is mandatory.")

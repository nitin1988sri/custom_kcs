import frappe

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
def get_employee_count(branch, role):
    count = frappe.db.count("Employee", filters={"branch": branch, "designation": role})
    return count
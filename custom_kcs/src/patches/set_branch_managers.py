import csv
import frappe

def run():
    csv_path = frappe.get_site_path("public", "files", "branch_managers.csv")

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            branch_name = row.get("Branch Name", "").strip()
            manager_name = row.get("Manager Name", "").strip()

            if not branch_name or not manager_name:
                print(f"⚠️ Skipping invalid row: {row}")
                continue

            # Find branch by branch_name field
            branch_id = frappe.db.get_value("Branch", {"branch_name": branch_name}, "name")
            if not branch_id:
                print(f"❌ Branch not found: {branch_name}")
                continue

            # Get employee ID using employee_name
            employee_id = frappe.db.get_value("Employee", {"employee_name": manager_name}, "name")
            if not employee_id:
                print(f"❌ Employee not found for manager: {manager_name}")
                continue

            try:
                branch_doc = frappe.get_doc("Branch", branch_id)
                branch_doc.branch_manager = employee_id
                branch_doc.save(ignore_permissions=True)
                frappe.db.commit()
                print(f"✅ Set manager '{manager_name}' (EmpID: {employee_id}) for branch: {branch_name}")
            except Exception as e:
                print(f"❌ Failed to update branch {branch_name}: {e}")

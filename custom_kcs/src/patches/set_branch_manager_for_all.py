import frappe

def run():
    try:
        manager_id = "HR-EMP-00459"

        # Check if this employee exists
        if not frappe.db.exists("Employee", manager_id):
            print(f"❌ Employee {manager_id} not found.")
            return

        # Update all branches with this manager
        frappe.db.set_value("Branch", {}, "branch_manager", manager_id)
        print(f"✅ All branches updated with branch_manager = {manager_id}")

    except Exception as e:
        print(f"❌ Error during branch manager migration: {e}")

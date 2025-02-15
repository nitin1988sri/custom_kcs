import frappe
from frappe.utils import nowdate

def revert_expired_transfers():
    transfers = frappe.get_all("Temporary Transfer", filters={"end_date": ["<=", nowdate()], "transfer_status": "Active"}, fields=["name", "employee", "original_branch"])

    for transfer in transfers:
        # Fetch Employee
        employee = frappe.get_doc("Employee", transfer["employee"])

        # Revert Employee to Original Branch
        employee.assigned_branch = transfer["original_branch"]
        employee.save()

        # Mark Transfer as Completed
        frappe.db.set_value("Temporary Transfer", transfer["name"], "transfer_status", "Completed")
        frappe.db.commit()

    return f"{len(transfers)} employees reverted to their original branches."


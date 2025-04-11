import frappe

def add_storage_fields():
    for field in [
        {"fieldname": "selected_customers", "label": "Selected Customers", "fieldtype": "Small Text", "hidden": 1},
        {"fieldname": "selected_branches", "label": "Selected Branches", "fieldtype": "Small Text", "hidden": 1},
    ]:
        if not frappe.db.exists("Custom Field", f"Payroll Entry-{field['fieldname']}"):
            cf = frappe.new_doc("Custom Field")
            cf.dt = "Payroll Entry"
            cf.fieldname = field["fieldname"]
            cf.label = field["label"]
            cf.fieldtype = field["fieldtype"]
            cf.hidden = field["hidden"]
            cf.insert_after = "employees"
            cf.save()
            frappe.db.commit()

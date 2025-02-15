import frappe

def add_client_field_to_employee():
    if not frappe.db.exists("DocType", "Employee"):
        print("Employee doctype does not exist!")
        return

    if not frappe.db.exists("Custom Field", {"dt": "Employee", "fieldname": "client"}):
        custom_field = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Employee",
            "fieldname": "client",
            "fieldtype": "Link",
            "label": "Client",
            "options": "Customer",
            "insert_after": "designation",
            "reqd": 1
        })
        custom_field.insert()
        frappe.db.commit()
        print("Client field added to Employee doctype.")
    else:
        print("Client field already exists in Employee doctype.")

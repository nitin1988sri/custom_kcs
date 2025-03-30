import frappe

def add_client_field_to_branch():
    if not frappe.db.exists("Custom Field", "Branch-client"):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Branch",
            "fieldname": "client",
            "label": "Client",
            "fieldtype": "Link",
            "options": "Customer",  
            "insert_after": "branch_name",
            "reqd":1
        }).insert()
        frappe.db.commit()
        print("✅ Client field added successfully to Branch doctype.")

import frappe

def create_temporary_transfer_doctype():
    if frappe.db.exists("DocType", "Temporary Transfer"):
        print("Doctype 'Temporary Transfer' already exists!")
        return

    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "Temporary Transfer",
        "module": "Custom Kcs",  
        "custom": 1,
        "fields": [
            {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "Employee", "reqd": 1},
            {"fieldname": "original_branch", "label": "Original Branch", "fieldtype": "Link", "options": "Branch", "reqd": 1},
            {"fieldname": "temporary_branch", "label": "Temporary Branch", "fieldtype": "Link", "options": "Branch", "reqd": 1},
            {"fieldname": "start_date", "label": "Start Date", "fieldtype": "Date", "reqd": 1},
            {"fieldname": "end_date", "label": "End Date", "fieldtype": "Date", "reqd": 1},
            {"fieldname": "billing_rate", "label": "Billing Rate at Temporary Branch", "fieldtype": "Currency", "reqd": 1},
            {"fieldname": "transfer_status", "label": "Transfer Status", "fieldtype": "Select", "options": "Active\nCompleted", "reqd": 1}
        ],
        "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
    })
    
    doctype.insert(ignore_if_duplicate=True)
    print("Temporary Transfer Doctype created successfully!")

create_temporary_transfer_doctype()

import frappe

def create_overtime_doctype():
    if frappe.db.exists("DocType", "Overtime"):
        print("Doctype 'Overtime' already exists!")
        return

    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "Overtime",
        "module": "Custom Kcs",  
        "custom": 1,
        "fields": [
            {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "Employee", "reqd": 1},
            {"fieldname": "original_branch", "label": "Original Branch", "fieldtype": "Link", "options": "Branch", "reqd": 1},
            {"fieldname": "overtime_branch", "label": "Overtime Branch", "fieldtype": "Link", "options": "Branch", "reqd": 1},
            {"fieldname": "start_date", "label": "Start Date", "fieldtype": "Date", "reqd": 1},
            {"fieldname": "shift_type", "label": "Shift", "fieldtype": "Link", "options": "Shift Type","reqd": 1},
            {"fieldname": "end_date", "label": "End Date", "fieldtype": "Date", "reqd": 1},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", "options": "Active\nCompleted", "reqd": 1}
        ],
        "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
    })
    
    doctype.insert(ignore_if_duplicate=True)
    print("Overtime Doctype created successfully!")

create_overtime_doctype()
def run_all():
    create_overtime_doctype()

run_all()    
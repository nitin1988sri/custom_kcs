import frappe

def add_shift_field():
    if not frappe.db.exists("Custom Field", "Employee-shift"):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Employee",
            "fieldname": "shift",
            "label": "Shift",
            "fieldtype": "Link",
            "options": "Shift Type",  
            "insert_after": "reports_to",  
            "reqd": 1,  
        }).insert()
        
        frappe.db.commit()
        print("Shift field added successfully to Employee doctype.")

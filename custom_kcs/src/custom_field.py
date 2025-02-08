import frappe

def create_employee_image_field():
    if not frappe.db.exists("Custom Field", {"dt": "Employee Checkin", "fieldname": "employee_image"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Employee Checkin",
            "fieldname": "employee_image",
            "label": "Employee Image",
            "fieldtype": "Attach Image",
            "insert_after": "time",
            "allow_on_submit": 1
        }).insert()
        frappe.db.commit()

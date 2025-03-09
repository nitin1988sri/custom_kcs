import frappe

def add_fields_to_employee_attendance():
    checkin_meta = frappe.get_doc("DocType", "Attendance")

    if not any(field.fieldname == "branch" for field in checkin_meta.fields):
        checkin_meta.append("fields", {
            "fieldname": "branch",
            "label": "Branch",
            "fieldtype": "Link",
            "options": "Branch",
            "reqd": 1  
        })

    if not any(field.fieldname == "work_location" for field in checkin_meta.fields):
        checkin_meta.append("fields", {
            "fieldname": "work_location",
            "label": "Work Location",
            "fieldtype": "Data",  
            "reqd": 1 
        })

    checkin_meta.save()
    frappe.db.commit()
    print("Fields added successfully!")

add_fields_to_employee_attendance()

import frappe

def add_fields_to_employee_checkin():
    # Load the "Employee Checkin" Doctype
    checkin_meta = frappe.get_doc("DocType", "Employee Checkin")

    # Check if "branch" field exists, if not, add it
    if not any(field.fieldname == "branch" for field in checkin_meta.fields):
        checkin_meta.append("fields", {
            "fieldname": "branch",
            "label": "Branch",
            "fieldtype": "Link",
            "options": "Branch",
            "reqd": 1  # Make it mandatory
        })

    # Check if "work_location" field exists, if not, add it
    if not any(field.fieldname == "work_location" for field in checkin_meta.fields):
        checkin_meta.append("fields", {
            "fieldname": "work_location",
            "label": "Work Location",
            "fieldtype": "Data",  # Change to "Link" if linking to another doctype
            "reqd": 1  # Make it mandatory
        })

    # Save the updated doctype
    checkin_meta.save()
    frappe.db.commit()
    print("Fields added successfully!")

# Run the function
add_fields_to_employee_checkin()

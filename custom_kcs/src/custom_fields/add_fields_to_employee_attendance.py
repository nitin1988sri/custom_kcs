import frappe

def add_custom_fields_to_attendance():
    custom_fields = {
        "Attendance": [
            {
                "fieldname": "branch",
                "label": "Branch",
                "fieldtype": "Link",
                "options": "Branch",
                "reqd": 1,
                "insert_after": "employee",
            },
            {
                "fieldname": "work_location",
                "label": "Work Location",
                "fieldtype": "Data",
                "insert_after": "branch",
            }
        ]
    }

    for doctype, fields in custom_fields.items():
        doctype_meta = frappe.get_meta(doctype)  # Get Doctype Metadata
        
        for field in fields:
            # Check if field exists in Doctype OR Custom Field
            if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}) or \
               field["fieldname"] in [df.fieldname for df in doctype_meta.fields]:
                print(f"⚠️ Field {field['fieldname']} already exists in {doctype}, skipping.")
            else:
                custom_field = frappe.get_doc({
                    "doctype": "Custom Field",
                    "dt": doctype,
                    **field
                })
                custom_field.insert()
                print(f"✅ Added custom field: {field['fieldname']} to {doctype}")

    frappe.db.commit()

add_custom_fields_to_attendance()

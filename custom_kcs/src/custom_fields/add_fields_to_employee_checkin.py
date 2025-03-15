import frappe

def add_custom_fields():
    custom_fields = {
        "Employee Checkin": [
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
                "reqd": 1,
                "insert_after": "branch",
            },
            {
                "fieldname": "shift_type",
                "label": "Shift Type",
                "fieldtype": "Link",
                "options": "Shift Type",
                "reqd": 1,
                "insert_after": "work_location",
            }
        ]
    }

    for doctype, fields in custom_fields.items():
        for field in fields:
            # Check if field already exists
            if not frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}):
                custom_field = frappe.get_doc({
                    "doctype": "Custom Field",
                    "dt": doctype,
                    **field
                })
                custom_field.insert()
                print(f"✅ Added custom field: {field['fieldname']} to {doctype}")
            else:
                print(f"⚠️ Field {field['fieldname']} already exists in {doctype}, skipping.")

    frappe.db.commit()

add_custom_fields()

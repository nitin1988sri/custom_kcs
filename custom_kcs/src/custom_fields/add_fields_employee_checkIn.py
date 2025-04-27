import frappe

def add_fields_to_employee_checkin():
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
                "fieldname": "shift_type",
                "label": "Shift Type",
                "fieldtype": "Link",
                "options": "Shift Type",
                "reqd": 1,
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

    
def run_all():
    add_fields_to_employee_checkin()
    create_employee_image_field()

run_all()        

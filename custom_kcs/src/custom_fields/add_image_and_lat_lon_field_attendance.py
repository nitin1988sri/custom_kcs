import frappe

def add_image_lat_lon_attendance_fields():
    fields = [
        {
            "label": "Latitude",
            "fieldname": "latitude",
            "fieldtype": "Float",
            "insert_after": "status",
        },
        {
            "label": "Longitude",
            "fieldname": "longitude",
            "fieldtype": "Float",
            "insert_after": "latitude",
        },
        {
            "label": "Photo",
            "fieldname": "image",
            "fieldtype": "Attach Image",
            # don't insert after a field that doesn't exist
            "insert_after": "longitude",
        },
    ]

    for field in fields:
        if not frappe.db.exists("Custom Field", {"dt": "Attendance", "fieldname": field["fieldname"]}):
            doc = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Attendance",
                **field
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"Created field: {field['fieldname']}")
        else:
            print(f"Field already exists: {field['fieldname']}")

def run_all():
    add_image_lat_lon_attendance_fields()

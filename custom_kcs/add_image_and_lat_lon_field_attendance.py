# apps/custom_kcs/custom_kcs/custom_fields/add_attendance_geo_fields.py

from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    custom_fields = {
        "Attendance": [
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
                "insert_after": "longitude",  
            },
        ]
    }
    create_custom_fields(custom_fields, ignore_validate=True)

def run_all():
    execute()


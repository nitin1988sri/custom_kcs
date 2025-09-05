import frappe

def add_image_lat_lon_attendance_fields():
    fields = [
        {
            "label": "Latitude",
            "fieldname": "latitude",
            "fieldtype": "Float",
            "insert_after": "status"
        },
        {
            "label": "Longitude",
            "fieldname": "longitude",
            "fieldtype": "Float",
            "insert_after": "latitude"
        },
        # {
        #     "label": "Branch Latitude",
        #     "fieldname": "branch_lat",
        #     "fieldtype": "Float",
        #     "insert_after": "longitude"
        # },
        # {
        #     "label": "Branch Longitude",
        #     "fieldname": "branch_lng",
        #     "fieldtype": "Float",
        #     "insert_after": "branch_lat"
        # },
        # {
        #     "label": "Distance (Meters)",
        #     "fieldname": "distance_m",
        #     "fieldtype": "Float",
        #     "insert_after": "branch_lng"
        # },
        {
            "label": "Photo",
            "fieldname": "image",
            "fieldtype": "Attach Image",
            "insert_after": "distance_m"
        }
    ]

    for field in fields:
        if not frappe.db.exists("Custom Field", {"dt": "Attendance", "fieldname": field["fieldname"]}):
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Attendance",
                **field
            }).insert()
            print(f"Created field: {field['fieldname']}")
        else:
            print(f"Field already exists: {field['fieldname']}")

def run_all():
    add_image_lat_lon_attendance_fields()

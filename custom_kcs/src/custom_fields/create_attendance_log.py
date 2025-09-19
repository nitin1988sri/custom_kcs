import frappe
from frappe.model.document import Document

def execute():
    if not frappe.db.exists("DocType", "Attendance Log"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Attendance Log",
            "module": "Custom KCS",  # अपने module का नाम डालें
            "custom": 1,
            "fields": [
                {
                    "fieldname": "employee",
                    "label": "Employee",
                    "fieldtype": "Link",
                    "options": "Employee",
                    "reqd": 1
                },
                {
                    "fieldname": "status",
                    "label": "Status",
                    "fieldtype": "Data",
                    "reqd": 1
                },
                {
                    "fieldname": "attendance_date",
                    "label": "Attendance Date",
                    "fieldtype": "Date"
                },
                {
                    "fieldname": "shift_type",
                    "label": "Shift Type",
                    "fieldtype": "Link",
                    "options": "Shift Type"
                },
                {
                    "fieldname": "branch",
                    "label": "Branch",
                    "fieldtype": "Link",
                    "options": "Branch"
                },
                {
                    "fieldname": "latitude",
                    "label": "Latitude",
                    "fieldtype": "Float"
                },
                {
                    "fieldname": "longitude",
                    "label": "Longitude",
                    "fieldtype": "Float"
                },
                {
                    "fieldname": "base64_image",
                    "label": "Base64 Image",
                    "fieldtype": "Long Text"
                },
                {
                    "fieldname": "filename",
                    "label": "Filename",
                    "fieldtype": "Data"
                },
                {
                    "fieldname": "raw_request",
                    "label": "Raw Request",
                    "fieldtype": "Long Text"
                }
            ],
            "permissions": [
                {
                    "role": "System Manager",
                    "read": 1,
                    "write": 1,
                    "create": 1,
                    "delete": 1
                }
            ]
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

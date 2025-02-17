import frappe

def create_shift_log_doctype():
    if not frappe.db.exists("DocType", "Shift Log"):
        shift_log = frappe.get_doc({
            "doctype": "DocType",
            "name": "Shift Log",
            "module": "Custom Kcs",
            "custom": 1,  # Mark as custom doctype
            "fields": [
                {
                    "fieldname": "employee",
                    "label": "Employee",
                    "fieldtype": "Link",
                    "options": "Employee",
                    "reqd": 1
                },
                {
                    "fieldname": "branch",
                    "label": "Branch",
                    "fieldtype": "Link",
                    "options": "Branch",
                    "reqd": 1
                },
                {
                    "fieldname": "work_location",
                    "label": "Work Location",
                    "fieldtype": "Data",
                    "reqd": 0
                },
                {
                    "fieldname": "shift_type",
                    "label": "Shift Type",
                    "fieldtype": "Link",
                    "options": "Shift Type",
                    "reqd": 1
                },
                {
                    "fieldname": "check_in_time",
                    "label": "Check-in Time",
                    "fieldtype": "Datetime",
                    "reqd": 1
                },
                {
                    "fieldname": "check_out_time",
                    "label": "Check-out Time",
                    "fieldtype": "Datetime",
                    "reqd": 0
                }
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
            ]
        })

        shift_log.insert()
        frappe.db.commit()
        print("✅ Shift Log Doctype Created Successfully!")
    else:
        print("⚠️ Shift Log Doctype Already Exists!")

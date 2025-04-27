import frappe

def add_new_doctype_attendances_status():
    if not frappe.db.exists('DocType', 'Attendance Status'):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Attendance Status",
            "module": "Custom KCS",
            "custom": 1,
            "fields": [
                {
                    "fieldname": "status_name",
                    "fieldtype": "Data",
                    "label": "Status Name",
                    "reqd": 1
                },
                {
                    "fieldname": "is_active",
                    "fieldtype": "Check",
                    "label": "Is Active",
                    "default": 1
                },
                {
                    "fieldname": "is_default",
                    "fieldtype": "Check",
                    "label": "Is Default"
                }
            ],
            "permissions": [
                {
                    "role": "System Manager",
                    "permlevel": 0,
                    "read": 1,
                    "write": 1,
                    "create": 1,
                    "delete": 1
                }
            ],
            "is_submittable": 0,
            "editable_grid": 1
        })
        doc.insert()
        frappe.db.commit()

def link_doctyp_to_Attendance():
    # Check if field exists
    meta = frappe.get_meta('Attendance')
    fieldnames = [f.fieldname for f in meta.fields]

    if 'status' in fieldnames:
        frappe.db.sql("""
            UPDATE `tabDocField`
            SET fieldtype = 'Link',
                options = 'Attendance Status'
            WHERE parent = 'Attendance' AND fieldname = 'status'
        """)
        frappe.clear_cache(doctype='Attendance')
        print("✅ Status field converted to Link field.")
    else:
        print("⚠️ Status field not found in Attendance Doctype.")        

def run_all():
    add_new_doctype_attendances_status()
    link_doctyp_to_Attendance()

run_all()    
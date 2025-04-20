import frappe

def create_equipment_master():
    if not frappe.db.exists("DocType", "Equipment Master"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Equipment Master",
            "module": "Custom Kcs",
            "custom": 1,
            "autoname": "field:equipment_name",
            "fields": [
                {
                    "fieldname": "equipment_name",
                    "label": "Equipment Name",
                    "fieldtype": "Data",
                    "reqd": 1
                },
                {
                    "fieldname": "description",
                    "label": "Description",
                    "fieldtype": "Small Text"
                }
            ],
            "permissions": [
                {
                    "role": "System Manager",
                    "read": 1, "write": 1, "create": 1, "delete": 1
                },
                {
                    "role": "Employee",
                    "read": 1
                }
            ]
        })
        doc.insert()
        frappe.db.commit()
        print("✅ Created Equipment Master Doctype.")


def create_equipment_allocation():
    if not frappe.db.exists("DocType", "Equipment Allocation"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Equipment Allocation",
            "module": "Custom Kcs",
            "custom": 1,
            "autoname": "field:employee",
            "fields": [
                {
                    "fieldname": "employee",
                    "label": "Employee",
                    "fieldtype": "Link",
                    "options": "Employee",
                    "reqd": 1
                },
                {
                    "fieldname": "equipment",
                    "label": "Equipment",
                    "fieldtype": "Link",
                    "options": "Equipment Master",
                    "reqd": 1
                },
                {
                    "fieldname": "allocation_date",
                    "label": "Allocation Date",
                    "fieldtype": "Date",
                    "reqd": 1
                },
                {
                    "fieldname": "return_date",
                    "label": "Return Date",
                    "fieldtype": "Date"
                },
                {
                    "fieldname": "condition",
                    "label": "Condition",
                    "fieldtype": "Select",
                    "options": "New\nGood\nAverage\nDamaged"
                },
                {
                    "fieldname": "remarks",
                    "label": "Remarks",
                    "fieldtype": "Small Text"
                }
            ],
            "permissions": [
                {
                    "role": "System Manager",
                    "read": 1, "write": 1, "create": 1, "delete": 1
                },
                {
                    "role": "Employee",
                    "read": 1
                }
            ]
        })
        doc.insert()
        frappe.db.commit()
        print("✅ Created Equipment Allocation Doctype.")

def execute():
    create_equipment_master()
    create_equipment_allocation()

def run_all():
    execute()

run_all()

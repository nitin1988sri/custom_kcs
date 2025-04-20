import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

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

def equipment_allocated():
    custom_fields = {
        "Equipment Allocation": [
            {
                "fieldname": "status",
                "label": "Status",
                "fieldtype": "Select",
                "options": "Requested\nAllocated\nReturned",
                "insert_after": "return_date",
                "reqd": 1,
                "default": "Allocated"
            }
        ]
    }
    create_custom_fields(custom_fields)

def allocation_naming_series():
    if frappe.db.exists("DocType", "Equipment Allocation"):
        frappe.db.set_value("DocType", "Equipment Allocation", "autoname", "naming_series:")

    if not frappe.db.exists("Custom Field", "Equipment Allocation-naming_series"):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Equipment Allocation",
            "fieldname": "naming_series",
            "fieldtype": "Data",
            "label": "Naming Series",
            "insert_after": "employee",
            "default": "EQA-.####",
            "reqd": 1
        }).insert()

    frappe.clear_cache(doctype="Equipment Allocation")

def remove_unique_from_employee_field():
    field = frappe.db.get_value("DocField", {
        "parent": "Equipment Allocation",
        "fieldname": "employee"
    }, "name")

    if field:
        frappe.db.set_value("DocField", field, "unique", 0)
        frappe.db.commit()
        frappe.clear_cache(doctype="Equipment Allocation")
        print("✅ Unique constraint removed from standard employee field.")
    else:
        print("❌ Field not found.")

# Run it
remove_unique_from_employee_field()    
def execute():
    create_equipment_master()
    create_equipment_allocation()
    equipment_allocated()
    allocation_naming_series()
    remove_unique_from_employee_field()

def run_all():
    execute()

run_all()

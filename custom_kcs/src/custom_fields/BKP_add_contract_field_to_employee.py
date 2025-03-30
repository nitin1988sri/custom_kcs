import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def add_contract_field_to_employee():
    custom_fields = {
        "Employee": [
            {
                "fieldname": "contract",
                "label": "Contract",
                "fieldtype": "Link",
                "options": "Contract",
                "insert_after": "branch", 
                "reqd": 1
            }
        ]
    }

    create_custom_fields(custom_fields)

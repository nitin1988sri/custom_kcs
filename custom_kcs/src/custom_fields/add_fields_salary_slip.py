from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    custom_fields = {
        "Salary Slip": [
            {
                "label": "Is Client Slip",
                "fieldname": "is_client_slip",
                "fieldtype": "Check",
                "insert_after": "salary_structure", 
                "default": "0"
            }
        ]
    }
    create_custom_fields(custom_fields)
def run_all():
    execute()

run_all()
  
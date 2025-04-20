from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def add_customer_to_salary_structure():
    create_custom_fields({
        "Salary Structure": [
            {
                "fieldname": "customer",
                "label": "Customer",
                "fieldtype": "Link",
                "options": "Customer",
                "insert_after": "company" 
            }
        ]
    })

def run_all():
    add_customer_to_salary_structure()

run_all()
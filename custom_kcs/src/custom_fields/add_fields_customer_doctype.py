import frappe

def create_customer_custom_fields():
    custom_fields = {
        "Customer": [
            {
                "fieldname": "gstin",
                "label": "GSTIN",
                "fieldtype": "Data",
                "insert_after": "tax_id"
            },
            {
                "fieldname": "secondary_contact_person",
                "label": "Secondary Contact Person",
                "fieldtype": "Data",
                "insert_after": "customer_primary_contact"
            },
            {
                "fieldname": "secondary_contact_mobile",
                "label": "Secondary Contact Mobile",
                "fieldtype": "Phone",
                "insert_after": "secondary_contact_person"
            },
            {
                "fieldname": "secondary_contact_email",
                "label": "Secondary Contact Email",
                "fieldtype": "Data",
                "insert_after": "secondary_contact_mobile"
            },
            {
                "fieldname": "assigned_units",
                "label": "Assigned Units",
                "fieldtype": "Table MultiSelect",
                "options": "Unit",
                "insert_after": "customer_group"
            }
        ]
    }

    from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
    create_custom_fields(custom_fields)

def run_all():
    create_customer_custom_fields()

run_all()
# This script creates custom fields in the Customer doctype.
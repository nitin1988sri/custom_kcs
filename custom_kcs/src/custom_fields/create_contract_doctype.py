import frappe

def create_custom_fields():
    custom_fields = {
        "Contract": [
            {
                "fieldname": "additional_details_section",
                "label": "Additional Details",
                "fieldtype": "Section Break",
                "insert_after": "end_date"
            },
            {
                "fieldname": "contract_code",
                "label": "Contract Code",
                "fieldtype": "Data",
                "insert_after": "additional_details_section",
                "reqd": 1,
                "unique": 1
            },
            {
                "fieldname": "branch",
                "label": "Branch",
                "fieldtype": "Link",
                "options": "Branch",
                "insert_after": "contract_code",
                "reqd": 1,
            },
            {
                "fieldname": "work_location",
                "label": "Work Location",
                "fieldtype": "Data",
                "insert_after": "branch"
            },
            {
                "fieldname": "contract_document",
                "label": "Contract Document",
                "fieldtype": "Attach",
                "insert_after": "work_location"
            },
            {
                "fieldname": "monthly_contract_value",
                "label": "Monthly Contract Value",
                "fieldtype": "Currency",
                "insert_after": "contract_document"
            },
            {
                "fieldname": "payment_terms",
                "label": "Payment Terms",
                "fieldtype": "Select",
                "insert_after": "monthly_contract_value",
                "options": "On Receipt\n3 Days\n7 Days"
            },
            {
                "fieldname": "additional_details_end",
                "fieldtype": "Section Break",
                "insert_after": "payment_terms"
            },

            # ✅ Separate Section for Roles
            {
                "fieldname": "roles_section",
                "label": "Roles Information",
                "fieldtype": "Section Break",
                "insert_after": "additional_details_end"
            },
            {
                "fieldname": "roles",
                "label": "Roles",
                "fieldtype": "Table",
                "insert_after": "roles_section",
                "options": "Contract Role"
            }
        ]
    }

    from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
    create_custom_fields(custom_fields)

create_custom_fields()

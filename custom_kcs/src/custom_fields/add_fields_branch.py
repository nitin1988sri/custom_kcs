import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_custom_fields_for_branch():
    fields = [
        {
            "fieldname": "client",
            "label": "Client",
            "fieldtype": "Link",
            "options": "Customer",
            "insert_after": "branch_name",
            "reqd": 1
        },
        {
            "fieldname": "city",
            "label": "City",
            "fieldtype": "Data",
            "insert_after": "client",
            "reqd": 1
        },
        {
            "fieldname": "state",
            "label": "State",
            "fieldtype": "Data",
            "insert_after": "city",
            "reqd": 1
        },
        {
            "fieldname": "linked_client",
            "label": "Linked Client",
            "fieldtype": "Link",
            "options": "Customer",
            "insert_after": "state"
        },
        {
            "fieldname": "contact_name",
            "label": "Contact Name",
            "fieldtype": "Data",
            "insert_after": "linked_client",
            "reqd": 1
        },
        {
            "fieldname": "contact_phone",
            "label": "Phone",
            "fieldtype": "Data",
            "insert_after": "contact_name",
            "reqd": 1
        },
        {
            "fieldname": "contact_email",
            "label": "Email",
            "fieldtype": "Data",
            "insert_after": "contact_phone"
        },
        {
            "fieldname": "branch_manager",
            "label": "Branch Manager",
            "fieldtype": "Link",
            "options": "Employee",
            "insert_after": "Email",
            "reqd": 1
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Select",
            "options": "Active\nInactive",
            "insert_after": "contact_email"
        },
        {
            "fieldname": "roles_employees_section",
            "label": "Roles & Employees",
            "fieldtype": "Section Break",
            "insert_after": "status"
        },
        {
            "fieldname": "roles",
            "label": "Roles",
            "fieldtype": "Table",
            "options": "Contract Role",
            "insert_after": "roles_employees_section"
        },
        {
            "fieldname": "employees_list",
            "label": "Employees List",
            "fieldtype": "Table",
            "options": "Employee Detail",
            "insert_after": "roles"
        }
    ]

    for field in fields:
        create_custom_field("Branch", field)

    frappe.db.commit()
    print("✅ Fields created with single bottom section for Roles & Employees")

# Run
create_custom_fields_for_branch()

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_custom_fields_for_branch():
    fields = [
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

def add_linked_contract_field():
    if not frappe.db.exists("Custom Field", "Branch-linked_contract"):
        doc = frappe.new_doc("Custom Field")
        doc.dt = "Branch"
        doc.label = "Linked Contract"
        doc.fieldname = "linked_contract"
        doc.fieldtype = "Link"
        doc.options = "Contract"
        doc.read_only = 1
        doc.insert_after = "status"  
        doc.save()
        frappe.db.commit()


def run_all():
    create_custom_fields_for_branch()
    add_linked_contract_field()

run_all()

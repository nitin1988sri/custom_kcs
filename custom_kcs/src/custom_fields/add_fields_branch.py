import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

# def create_custom_fields_for_branch():
#     fields = [
#         {
#            "fieldname": "city",
#             "label": "City",
#             "fieldtype": "Link",
#             "options": "City",
#             "insert_after": "client",
#             "reqd": 1
#         },
#         {
#             "fieldname": "state",
#             "label": "State",
#             "fieldtype": "Link",
#             "options": "State",
#             "insert_after": "city",
#             "reqd": 1
#         },
#         {
#             "fieldname": "contact_name",
#             "label": "Contact Name",
#             "fieldtype": "Data",
#             "insert_after": "linked_client",
#             "reqd": 1
#         },
#         {
#             "fieldname": "contact_phone",
#             "label": "Phone",
#             "fieldtype": "Data",
#             "insert_after": "contact_name",
#             "reqd": 1
#         },
#         {
#             "fieldname": "contact_email",
#             "label": "Email",
#             "fieldtype": "Data",
#             "insert_after": "contact_phone"
#         },
#         {
#             "fieldname": "branch_manager",
#             "label": "Branch Manager",
#             "fieldtype": "Link",
#             "options": "Employee",
#             "insert_after": "Email",
#             "reqd": 1
#         },
#         {
#             "fieldname": "status",
#             "label": "Status",
#             "fieldtype": "Select",
#             "options": "Active\nInactive",
#             "insert_after": "contact_email"
#         },
#         {
#             "fieldname": "roles_employees_section",
#             "label": "Roles & Employees",
#             "fieldtype": "Section Break",
#             "insert_after": "status"
#         },
#         {
#             "fieldname": "roles",
#             "label": "Roles",
#             "fieldtype": "Table",
#             "options": "Contract Role",
#             "insert_after": "roles_employees_section"
#         },
#         {
#             "fieldname": "employees_list",
#             "label": "Employees List",
#             "fieldtype": "Table",
#             "options": "Employee Detail",
#             "insert_after": "roles"
#         }
#     ]

#     for field in fields:
#         create_custom_field("Branch", field)

#     frappe.db.commit()
#     print("✅ Fields created with single bottom section for Roles & Employees")

def create_branch_doctype():
    if frappe.db.exists("DocType", "Branch"):
        print("⚠️ 'Branch' Doctype already exists.")
        return

    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Branch",
        "module": "Custom Kcs", 
        "custom": 0,
        "autoname": "field:branch_name",
        "fields": [
            {
                "fieldname": "branch_name",
                "label": "Branch Name",
                "fieldtype": "Data",
                "reqd": 1
            },
            {
                "fieldname": "old_branch_code",
                "label": "Old Branch Code",
                "fieldtype": "Data",
                "insert_after": "branch_name",
                "reqd": 0
            },
            {
                "fieldname": "client",
                "label": "Client",
                "fieldtype": "Link",
                "options": "Customer",
                "reqd": 1
            },
            {
                "fieldname": "state",
                "label": "State",
                "fieldtype": "Link",
                "options": "State",
                "reqd": 1
            },
            {
                "fieldname": "city",
                "label": "City",
                "fieldtype": "Link",
                "options": "City",
                "reqd": 1
            },
            {
                "fieldname": "billing_location",
                "label": "Billing Location",
                "fieldtype": "Small Text",
                "insert_after": "city",  
                "reqd": 0
            },
            {
                "fieldname": "gst",
                "label": "GST",
                "fieldtype": "Data",
                "insert_after": "billing_location", 
                "reqd": 1
            },
            {
                "fieldname": "address",
                "label": "Address",
                "fieldtype": "Small Text",
                "insert_after": "billing_location", 
                "reqd": 1
            },
            {
                "fieldname": "contact_name",
                "label": "Contact Name",
                "fieldtype": "Data",
                "reqd": 1
            },
            {
                "fieldname": "contact_phone",
                "label": "Phone",
                "fieldtype": "Data",
                "reqd": 1
            },
            {
                "fieldname": "contact_email",
                "label": "Email",
                "fieldtype": "Data"
            },
            {
                "fieldname": "branch_manager",
                "label": "Branch Manager",
                "fieldtype": "Link",
                "options": "Employee",
                "reqd": 0
            },
            {
                "fieldname": "status",
                "label": "Status",
                "fieldtype": "Select",
                "options": "Active\nInactive"
            },
            {
                "fieldname": "roles_employees_section",
                "label": "Roles & Employees",
                "fieldtype": "Section Break"
            },
            {
                "fieldname": "roles",
                "label": "Roles",
                "fieldtype": "Table",
                "options": "Contract Role"
            },
            {
                "fieldname": "employees_list",
                "label": "Employees List",
                "fieldtype": "Table",
                "options": "Employee Detail"
            }
            
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
        ]
    })

    doc.insert()
    frappe.db.commit()
    print("✅ 'Branch' Doctype created successfully.")

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


def rename_branch_doctype_for_backup():
    old_name = "Branch"
    base_backup_name = "Branch Backup"
    backup_name = base_backup_name
    counter = 1

    # Check if original Doctype exists
    if not frappe.db.exists("DocType", old_name):
        print(f"❌ Doctype '{old_name}' does not exist.")
        return

    # Generate unique backup name
    while frappe.db.exists("DocType", backup_name):
        backup_name = f"{base_backup_name} {counter}"
        counter += 1

    # Rename the DocType
    frappe.rename_doc("DocType", old_name, backup_name, force=True)
    frappe.db.commit()
    print(f"✅ Renamed Doctype '{old_name}' to '{backup_name}'")

def run_all():
    #rename_branch_doctype_for_backup()
    create_branch_doctype()
    add_linked_contract_field()

run_all()

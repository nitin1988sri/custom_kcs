import frappe
from frappe.model.document import Document
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_contract_branch_doctype():
    if not frappe.db.exists("DocType", "Contract Branch"):
        doc = frappe.new_doc("DocType")
        doc.name = "Contract Branch"
        doc.module = "Custom Kcs"  
        doc.custom = 1
        doc.istable = 1  
        doc.append("fields", {
            "label": "Branch",
            "fieldname": "branch",
            "fieldtype": "Link",
            "options": "Branch",
        })

        doc.save()
        frappe.db.commit()
        print("✅ Contract Branch child doctype created.")
    else:
        print("ℹ️ Contract Branch already exists.")


# 🔹 Step 2: Create Contract Addendum child doctype
def create_contract_addendum_doctype():
    if not frappe.db.exists("DocType", "Contract Addendum"):
        doc = frappe.new_doc("DocType")
        doc.name = "Contract Addendum"
        doc.module = "Custom Kcs" 
        doc.custom = 1
        doc.istable = 1

        doc.append("fields", {
            "label": "Title",
            "fieldname": "title",
            "fieldtype": "Data",
        })
        doc.append("fields", {
            "label": "Start Date",
            "fieldname": "start_date",
            "fieldtype": "Date",
        })
        doc.append("fields", {
            "label": "End Date",
            "fieldname": "end_date",
            "fieldtype": "Date",
        })
        doc.append("fields", {
            "label": "Description",
            "fieldname": "description",
            "fieldtype": "Small Text"
        })
        doc.append("fields", {
            "label": "Document",
            "fieldname": "document",
            "fieldtype": "Attach",
        })

        doc.save()
        frappe.db.commit()
        print("✅ Contract Addendum child doctype created.")
    else:
        print("ℹ️ Contract Addendum already exists.")


# 🔹 Step 3: Add custom fields to Contract
def create_contract_custom_fields():
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
                "fieldname": "branches_section",
                "label": "Branches",
                "fieldtype": "Section Break",
                "insert_after": "contract_code"
            },
            {
                "fieldname": "contract_branches",
                "label": "Branches",
                "fieldtype": "Table",
                "options": "Contract Branch",  
                "insert_after": "branches_section"
            },
            {
                "fieldname": "work_location",
                "label": "Work Location",
                "fieldtype": "Data",
                "insert_after": "contract_branches"
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
            {
                "fieldname": "addendum_section",
                "label": "Contract Addendum",
                "fieldtype": "Section Break",
                "insert_after": "additional_details_end"
            },
            {
                "fieldname": "contract_addendums",
                "label": "Addendums",
                "fieldtype": "Table",
                "insert_after": "addendum_section",
                "options": "Contract Addendum"
            }
        ]
    }

    create_custom_fields(custom_fields)
    print("✅ Custom fields for Contract added.")

def add_mega_contract_field_to_contract():
    custom_fields = {
        "Contract": [
            {
                "fieldname": "mega_contract",
                "label": "Mega Contract",
                "fieldtype": "Link",
                "options": "Mega Contract",
                "insert_after": "contract_code"
            }
        ]
    }
    create_custom_fields(custom_fields)
    print("✅ Mega Contract field added to Contract")

def run_all():
    create_contract_branch_doctype()
    create_contract_addendum_doctype()
    create_contract_custom_fields()
    add_mega_contract_field_to_contract()

run_all()

import frappe

def create_linked_contract_child_table():
    if not frappe.db.exists("DocType", "Linked Contract"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Linked Contract",
            "module": "Custom Kcs",
            "custom": 1,
            "istable": 1,
            "fields": [
                {
                    "label": "Contract",
                    "fieldname": "contract",
                    "fieldtype": "Link",
                    "options": "Contract"
                }
            ],
            "permissions": [{
                "role": "System Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1
            }]
        })
        doc.insert()
        frappe.db.commit()
        print("✅ Linked Contract child table created.")
    else:
        print("ℹ️ Linked Contract already exists.")

def create_mega_contract_doctype():
    if not frappe.db.exists("DocType", "Mega Contract"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Mega Contract",
            "module": "Custom Kcs",
            "custom": 1,
            "istable": 0,
            "fields": [
                {
                    "label": "Mega Contract Title",
                    "fieldname": "title",
                    "fieldtype": "Data",
                    "reqd": 1
                },
                {
                    "label": "Contracts",
                    "fieldname": "linked_contracts",
                    "fieldtype": "Table",
                    "options": "Linked Contract",
                    "read_only": 1
                }
            ],
            "permissions": [{
                "role": "System Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1
            }]
        })
        doc.insert()
        frappe.db.commit()
        print("✅ Mega Contract Doctype created successfully!")
    else:
        print("ℹ️ Mega Contract already exists.")

def set_naming_by_title_for_mega_contract():
    if frappe.db.exists("DocType", "Mega Contract"):
        frappe.db.set_value(
            "DocType",
            "Mega Contract",
            "autoname",
            "field:title"
        )
        print("✅ Mega Contract autoname set to field:title")
    else:
        print("❌ Mega Contract Doctype not found.")

def set_naming_by_contract_for_linked_contract():
    if frappe.db.exists("DocType", "Linked Contract"):
        frappe.db.set_value(
            "DocType",
            "Linked Contract",
            "autoname",
            "field:contract"
        )
        frappe.db.set_value(
            "DocType",
            "Linked Contract",
            "naming_rule",
            "By fieldname"
        )
        print("✅ Linked Contract autoname set to field:contract and naming rule set to 'By fieldname'")
    else:
        print("❌ Linked Contract Doctype not found.")

def run_all():
    create_linked_contract_child_table()
    create_mega_contract_doctype()
    set_naming_by_title_for_mega_contract()
    set_naming_by_contract_for_linked_contract()
run_all()    
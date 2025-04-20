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
                    "options": "Linked Contract"
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

def run_all():
    create_linked_contract_child_table()
    create_mega_contract_doctype()
run_all()    
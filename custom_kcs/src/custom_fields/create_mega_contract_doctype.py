import frappe
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
        print("✅ Mega Contract Doctype created successfully!")
    else:
        print("ℹ️ Mega Contract already exists.")


def run_all():
    create_mega_contract_doctype()
run_all()    
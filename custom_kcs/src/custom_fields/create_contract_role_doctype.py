import frappe

def create_contract_role_doctype():
    if not frappe.db.exists("DocType", "Contract Role"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Contract Role",
            "module": "Custom Kcs",
            "custom": 1, 
            "istable": 1,  
            "fields": [
                {
                    "fieldname": "role",
                    "fieldtype": "Link",
                    "options": "Designation",
                    "label": "Role"
                },
                {
                    "fieldname": "no_of_personnel",
                    "fieldtype": "Int",
                    "label": "Number of Personnel"
                },
                {
                    "fieldname": "billing_rate",
                    "fieldtype": "Currency",
                    "label": "Billing Rate"
                }
            ],
            "engine": "InnoDB"
        })
        doc.insert()
        frappe.db.commit()
        print("✅ Contract Role Doctype created successfully!")
    else:
        print("⚠️ Contract Role Doctype already exists.")

# Run the function to create the Doctype
create_contract_role_doctype()

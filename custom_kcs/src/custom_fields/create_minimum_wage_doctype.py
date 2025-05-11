
import frappe
def create_minimum_wage_doctype():
    if frappe.db.exists("DocType", "Minimum Wage"):
        print("✅ Minimum Wage already exists.")
        return

    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Minimum Wage",
        "module": "Custom Kcs",
        "custom": 1,
        "fields": [
            {"fieldname": "state", "label": "State", "fieldtype": "Link", "options": "State", "reqd": 1},
            {"fieldname": "employment_class", "label": "Employment Class", "fieldtype": "Data", "reqd": 1},
            {"fieldname": "zone", "label": "Zone", "fieldtype": "Data"},
            {"fieldname": "effective_date", "label": "Effective Date", "fieldtype": "Date", "reqd": 1},
            {"fieldname": "basic", "label": "Basic", "fieldtype": "Currency"},
            {"fieldname": "vda", "label": "VDA", "fieldtype": "Currency"},
            {"fieldname": "hra", "label": "HRA", "fieldtype": "Currency"},
            {"fieldname": "total_min_wage", "label": "Total Min Wage", "fieldtype": "Currency", "read_only": 1}
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
        ]
    })
    doc.insert()
    print("✅ Minimum Wage Doctype created.")

def run_all():
    create_minimum_wage_doctype()
run_all()
# Run with:

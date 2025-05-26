import frappe

def create_city_doctype():
    if frappe.db.exists("DocType", "City"):
        print("✅ 'City' Doctype already exists.")
        return

    city_doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "City",
        "module": "Custom Kcs",
        "custom": 1,
        "istable": 0,
        "show_name_in_global_search": 1,
        "search_fields": "city_name",
        "title_field": "city_name",
        "fields": [
            {
                "fieldname": "state",
                "label": "State",
                "fieldtype": "Link",
                "options": "State",
                "reqd": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "city_name",
                "label": "City Name",
                "fieldtype": "Data",
                "reqd": 1,
                "in_list_view": 1
            }
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
        ]
    })
    city_doc.insert()
    frappe.db.commit()
    print("✅ 'City' Doctype created successfully.")

def run_all():
    create_city_doctype()
run_all()

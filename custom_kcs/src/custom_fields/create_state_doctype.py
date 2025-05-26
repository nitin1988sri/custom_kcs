import frappe

def create_state_doctype():
    if frappe.db.exists("DocType", "State"):
        print("✅ 'State' Doctype already exists.")
        return

    state_doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "State",
        "module": "Custom Kcs",
        "custom": 1,
        "istable": 0,
        "show_name_in_global_search": 1,
        "search_fields": "state_name",
        "title_field": "state_name",
        "fields": [
            {
                "fieldname": "country",
                "label": "Country",
                "fieldtype": "Link",
                "options": "Country",
                "default": "India",
                "reqd": 1,
                "in_list_view": 1
            },
            {
                "fieldname": "state_name",
                "label": "State Name",
                "fieldtype": "Data",
                "reqd": 1,
                "in_list_view": 1
            }
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
        ]
    })
    state_doc.insert()
    frappe.db.commit()
    print("✅ 'State' Doctype created successfully.")
    
def run_all():
    create_state_doctype()
run_all()
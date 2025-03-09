import frappe

def add_basic_incentive_amout_hidden_field_salary_slip():
    fields_to_add = [
        {
            "fieldname": "basic",
            "fieldtype": "Currency",
            "label": "Basic Salary",
            "insert_after": "gross_pay",
            "hidden": 1
        },
        {
            "fieldname": "incentive",
            "fieldtype": "Currency",
            "label": "Incentive Salary",
            "insert_after": "basic",
            "hidden": 1
        }
    ]

    for field in fields_to_add:
        if not frappe.db.exists("Custom Field", {"dt": "Salary Slip", "fieldname": field["fieldname"]}):
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Salary Slip",
                "fieldname": field["fieldname"],
                "fieldtype": field["fieldtype"],
                "label": field["label"],
                "insert_after": field["insert_after"],
                "read_only": 1,
                "hidden": 1  # Field will be hidden
            }).insert()

    frappe.db.commit()
    print("✅ Basic and Incentive Fields Added and Set to Hidden!")

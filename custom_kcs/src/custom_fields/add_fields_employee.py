import frappe

def add_client_field_to_employee():
    if not frappe.db.exists("DocType", "Employee"):
        print("Employee doctype does not exist!")
        return

    if not frappe.db.exists("Custom Field", {"dt": "Employee", "fieldname": "client"}):
        custom_field = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Employee",
            "fieldname": "client",
            "fieldtype": "Link",
            "label": "Client",
            "options": "Customer",
            "insert_after": "designation",
            "reqd": 1
        })
        custom_field.insert()
        frappe.db.commit()
        print("Client field added to Employee doctype.")
    else:
        print("Client field already exists in Employee doctype.")

def add_shift_field():
    if not frappe.db.exists("Custom Field", "Employee-shift"):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Employee",
            "fieldname": "shift",
            "label": "Shift",
            "fieldtype": "Link",
            "options": "Shift Type",  
            "insert_after": "reports_to",  
            "reqd": 1,  
        }).insert()
        
        frappe.db.commit()
        print("Shift field added successfully to Employee doctype.")


def add_field_esic_number_and_aadhaar_number_emp_salary_tab():
    fields = [
        {
            "fieldname": "esic_number",
            "label": "ESIC Number",
            "fieldtype": "Data",
            "insert_after": "ctc",  # Or "salary_currency"
            "reqd": 1,
            "section": "Salary"
        },
        {
            "fieldname": "aadhaar_number",
            "label": "Aadhaar Card Number",
            "fieldtype": "Data",
            "insert_after": "esic_number",
            "reqd": 1,
            "section": "Salary"
        }
    ]

    for field in fields:
        if not frappe.db.exists("Custom Field", f"Employee-{field['fieldname']}"):
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Employee",
                "fieldname": field["fieldname"],
                "label": field["label"],
                "fieldtype": field["fieldtype"],
                "insert_after": field["insert_after"],
                "reqd": field["reqd"],
                "depends_on": "",
                "hidden": 0,
                "is_custom_field": 1
            })
            custom_field.save()
            frappe.db.commit()

    frappe.msgprint("✅ ESIC and Aadhaar fields added to Employee.")

def run_all():
    add_client_field_to_employee()
    add_shift_field()
    add_field_esic_number_and_aadhaar_number_emp_salary_tab()

run_all()        

        

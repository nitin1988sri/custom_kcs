import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

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

def add_contract_series():
    try:
        # Get options from DocField
        options = frappe.db.get_value("DocField", {"parent": "Employee", "fieldname": "naming_series"}, "options") or ""

        series_list = options.strip().split("\n")

        if "HR-CONT-.###" not in series_list:
            series_list.append("HR-CONT-.###")
            updated_options = "\n".join(series_list)

            # Always create or update Property Setter
            prop = frappe.db.get_value(
                "Property Setter",
                {"doc_type": "Employee", "property": "options", "field_name": "naming_series"},
                "name"
            )

            if prop:
                frappe.db.set_value("Property Setter", prop, "value", updated_options)
            else:
                frappe.get_doc({
                    "doctype": "Property Setter",
                    "doc_type": "Employee",
                    "field_name": "naming_series",
                    "property": "options",
                    "value": updated_options,
                    "property_type": "Text",
                }).insert()

            frappe.db.commit()
            print("✅ HR-CONT-.### added to Employee naming_series")
        else:
            print("ℹ️ HR-CONT-.### already present")

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in add_contract_series_to_employee")
        print(f"❌ Error: {str(e)}")

def add_bank_passbook_attachment_field():
    custom_fields = {
        "Employee": [
            {
                "fieldname": "bank_passbook",
                "label": "Bank Passbook",
                "fieldtype": "Attach",
                "insert_after": "salary_mode",  # or any fieldname in 'Salary' section
                "depends_on": "",
                "read_only": 0,
                "reqd": 0
            }
        ]
    }

    create_custom_fields(custom_fields, update=True)

def add_some_more_fields():
    custom_fields = {
        "Employee": [
            {
                "fieldname": "fathers_name",
                "label": "Father's Name",
                "fieldtype": "Data",
                "insert_after": "full_name"
            },
            {
                "fieldname": "mothers_name",
                "label": "Mother's Name",
                "fieldtype": "Data",
                "insert_after": "fathers_name"
            },
            {
                "fieldname": "spouse_name",
                "label": "Spouse Name",
                "fieldtype": "Data",
                "depends_on": "eval:doc.marital_status == 'Married'",
                "insert_after": "marital_status"
            },
            {
                "fieldname": "aadhaar_card_front",
                "label": "Aadhar Details (Side 1)",
                "fieldtype": "Attach Image",
                "insert_after": "aadhaar_number"
            },
            {
                "fieldname": "aadhaar_card_back",
                "label": "Aadhar Details (Side 2)",
                "fieldtype": "Attach Image",
                "insert_after": "aadhaar_card_front"
            },
            {
                "fieldname": "pan_card",
                "label": "PAN Details",
                "fieldtype": "Attach Image",
                "insert_after": "pan_number"
            },
            {
                "fieldname": "uan_number",
                "label": "UAN Number",
                "fieldtype": "Data",
                "insert_after": "pan_card"
            },
            {
                "fieldname": "full_length_photo",
                "label": "Full Length Photo",
                "fieldtype": "Attach Image",
                "insert_after": "status"
            },
        ]
    }

    create_custom_fields(custom_fields)

def run_all():
    add_client_field_to_employee()
    add_shift_field()
    add_field_esic_number_and_aadhaar_number_emp_salary_tab()
    add_contract_series()
    add_bank_passbook_attachment_field()
    add_some_more_fields()

run_all()        

        

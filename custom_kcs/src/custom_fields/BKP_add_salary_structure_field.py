import frappe
from frappe.model.meta import get_meta

def add_salary_structure_field():
    doctype = "Contract Role"
    fieldname = "salary_structure"

    meta = get_meta(doctype)
    if any(df.fieldname == fieldname for df in meta.fields):
        print(f"Field '{fieldname}' already exists in {doctype}")
        return

    # Add new field
    frappe.get_doc({
        "doctype": "Custom Field",
        "dt": doctype,
        "fieldname": fieldname,
        "label": "Salary Structure",
        "fieldtype": "Link",
        "options": "Salary Structure",
        "insert_after": "billing_rate",  
    }).insert()

    print(f"Field '{fieldname}' added to {doctype} successfully.")

add_salary_structure_field()

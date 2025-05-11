import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_unit_doctype():
    if frappe.db.exists("DocType", "Unit"):
        print("Unit Doctype already exists")
        return

    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Unit",
        "module": "Custom Kcs",
        "custom": 1,
        "istable": 0,
        "autoname": "naming_series:",
        "naming_series": "UNIT-.#####",
        "fields": [
            {"fieldname": "naming_series", "label": "Naming Series", "fieldtype": "Select", "options": "UNIT-.#####", "reqd": 1},
            {"fieldname": "customer", "label": "Customer", "fieldtype": "Link", "options": "Customer", "reqd": 1},
            {"fieldname": "unit_name", "label": "Unit Name", "fieldtype": "Data", "reqd": 1},
            {"fieldname": "address", "label": "Address", "fieldtype": "Link", "options": "Address"},
            {"fieldname": "staff_in_charge", "label": "Staff In-Charge", "fieldtype": "Link", "options": "Employee", "reqd": 1},
            {"fieldname": "primary_customer_rep_name", "label": "Primary Customer Rep Name", "fieldtype": "Data", "reqd": 1},
            {"fieldname": "primary_customer_rep_mobile", "label": "Primary Customer Rep Mobile", "fieldtype": "Phone", "reqd": 1},
            {"fieldname": "primary_customer_rep_email", "label": "Primary Customer Rep Email", "fieldtype": "Data", "reqd": 1},
            {"fieldname": "secondary_customer_rep_name", "label": "Secondary Customer Rep Name", "fieldtype": "Data"},
            {"fieldname": "secondary_customer_rep_mobile", "label": "Secondary Customer Rep Mobile", "fieldtype": "Phone"},
            {"fieldname": "secondary_customer_rep_email", "label": "Secondary Customer Rep Email", "fieldtype": "Data"},
            {"fieldname": "main_contract", "label": "Main Contract", "fieldtype": "Link", "options": "Contract"},
            {"fieldname": "unit_contract", "label": "Unit Contract", "fieldtype": "Link", "options": "Contract"},
            {"fieldname": "credit_period_days", "label": "Credit Period (Days)", "fieldtype": "Int"},
            {"fieldname": "attendance_cycle_start_day", "label": "Attendance Cycle Start Day", "fieldtype": "Int"},
            {"fieldname": "attendance_cycle_end_logic", "label": "Attendance Cycle End Logic", "fieldtype": "Select", "options": "End of Month\nDay Before Start Day"},
            {"fieldname": "working_days_pattern", "label": "Working Days Pattern", "fieldtype": "Select", "options": "Mon-Sat (Sun Off)\nAll Days"},
            {"fieldname": "shift_type", "label": "Shift Type", "fieldtype": "Select", "options": "Single\nDouble\nTriple"},
            {"fieldname": "shifts", "label": "Shifts", "fieldtype": "Table", "options": "Unit Shift"},
            {"fieldname": "public_holidays", "label": "Public Holidays", "fieldtype": "Table", "options": "Unit Holiday"}
        ],
        "permissions": [
            {
                "role": "System Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1
            }
        ]
    })
    doc.insert()
    print("✅ Unit DocType created")

def run_all():
    create_unit_doctype()

run_all()    

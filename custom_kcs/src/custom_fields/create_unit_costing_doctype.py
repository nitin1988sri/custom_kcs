
import frappe
def create_unit_costing_doctype():
    if frappe.db.exists("DocType", "Unit Costing"):
        print("✅ Unit Costing already exists.")
        return

    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Unit Costing",
        "module": "Custom Kcs",
        "custom": 1,
        "fields": [
            {"fieldname": "unit", "label": "Unit", "fieldtype": "Link", "options": "Unit", "reqd": 1},
            {"fieldname": "employee_role", "label": "Employee Role", "fieldtype": "Link", "options": "Employee Role", "reqd": 1},
            {"fieldname": "effective_date", "label": "Effective Date", "fieldtype": "Date", "reqd": 1},
            {"fieldname": "linked_min_wage", "label": "Linked Min Wage", "fieldtype": "Link", "options": "Minimum Wage"},
            {"fieldname": "employment_class", "label": "Employment Class", "fieldtype": "Data"},
            {"fieldname": "zone", "label": "Zone", "fieldtype": "Data"},
            {"fieldname": "working_days_per_month", "label": "Working Days/Month", "fieldtype": "Int"},
            {"fieldname": "working_hours_per_day", "label": "Working Hours/Day", "fieldtype": "Int"},

            # Wage
            {"fieldname": "basic_cost", "label": "Basic Cost", "fieldtype": "Currency"},
            {"fieldname": "vda_cost", "label": "VDA Cost", "fieldtype": "Currency"},
            {"fieldname": "hra_cost", "label": "HRA Cost", "fieldtype": "Currency"},
            {"fieldname": "allowances_cost", "label": "Allowances Cost", "fieldtype": "Currency"},
            {"fieldname": "overtime_charges_cost", "label": "Overtime Charges", "fieldtype": "Currency"},
            {"fieldname": "relieving_charges_cost", "label": "Relieving Charges", "fieldtype": "Currency"},
            {"fieldname": "gross_salary_cost", "label": "Gross Salary Cost", "fieldtype": "Currency", "read_only": 1},

            # Compliances
            {"fieldname": "employer_pf_cost", "label": "Employer PF", "fieldtype": "Currency"},
            {"fieldname": "employer_esi_cost", "label": "Employer ESI", "fieldtype": "Currency"},
            {"fieldname": "bonus_cost", "label": "Bonus", "fieldtype": "Currency"},
            {"fieldname": "leave_encashment_cost", "label": "Leave Encashment", "fieldtype": "Currency"},
            {"fieldname": "national_holidays_cost", "label": "National Holidays", "fieldtype": "Currency"},
            {"fieldname": "gratuity_cost", "label": "Gratuity", "fieldtype": "Currency"},
            {"fieldname": "uniform_allowance_cost", "label": "Uniform Allowance", "fieldtype": "Currency"},
            {"fieldname": "total_monthly_cost", "label": "Total Monthly Cost", "fieldtype": "Currency", "read_only": 1},

            # Margin
            {"fieldname": "linked_unit_pricing", "label": "Linked Unit Pricing", "fieldtype": "Link", "options": "Unit Pricing"},
            {"fieldname": "monthly_margin", "label": "Monthly Margin", "fieldtype": "Currency", "read_only": 1},
            {"fieldname": "monthly_margin_percent", "label": "Margin %", "fieldtype": "Percent", "read_only": 1}
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
        ]
    })
    doc.insert()
    print("✅ Unit Costing Doctype created.")

def run_all():
    create_unit_costing_doctype()
run_all()
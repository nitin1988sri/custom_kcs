import frappe

def add_incentive_days_field_in_salary_slip():
    if not frappe.db.exists("Custom Field", {"dt": "Salary Slip", "fieldname": "incentive_days"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Salary Slip",
            "fieldname": "incentive_days",
            "fieldtype": "Int",
            "label": "Incentive Days",
            "insert_after": "payment_days",
            "read_only": 1
        }).insert()
        frappe.db.commit()
        print("✅ incentive_days field added successfully to Salary Slip!")
    else:
        print("⚠️ incentive_days field already exists. Skipping field creation.")

    print("✅ Moving forward...")

add_incentive_days_field_in_salary_slip()

print("🚀 Continuing with further execution...")

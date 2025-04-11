import frappe

def create_salary_paid_status_report():
    if not frappe.db.exists("Report", "Salary Paid Status"):
        report = frappe.get_doc({
            "doctype": "Report",
            "report_name": "Salary Paid Status",
            "ref_doctype": "Payroll Entry",
            "module": "Custom Kcs",
            "report_type": "Script Report",
            "is_standard": "No",
            "js": "custom_kcs/public/js/salary_paid_status.js"
        })
        report.insert()
        frappe.db.commit()
        print("✅ Salary Paid Status report created.")
    else:
        print("ℹ️ Report already exists.")

create_salary_paid_status_report()

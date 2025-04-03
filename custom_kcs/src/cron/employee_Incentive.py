import frappe
from frappe.utils import get_first_day, getdate, flt
from custom_kcs.src.empolyee_incentive import calculate_incentive_for_employee

@frappe.whitelist()
def generate_employee_incentives_for_all(start_date=None):
    if not start_date:
        start_date = get_first_day(getdate())

    employees = frappe.get_all("Employee", filters={"status": "Active"}, pluck="name")
    created_incentives = []

    for emp in employees:
        try:
            existing_incentive = frappe.db.exists("Employee Incentive", {
                "employee": emp,
                "payroll_date": start_date,
                "salary_component": "Incentive",
                "docstatus": ("!=", 2)
            })

            if existing_incentive:
                frappe.logger().info(f"Incentive already exists for {emp} on {start_date}")
                continue  

            result = calculate_incentive_for_employee(emp, start_date)
            frappe.logger().info(f"Result for {emp}: {result}")

            incentive_amount = result.get("incentive_amount", 0)
            incentive_days = result.get("incentive_days", 0)

            if not incentive_amount:
                continue

            doc = frappe.new_doc("Employee Incentive")
            doc.employee = emp
            doc.company = frappe.get_value("Employee", emp, "company")
            doc.department = frappe.get_value("Employee", emp, "department")
            doc.salary_component = "Incentive"
            doc.currency = "INR"
            doc.payroll_date = start_date
            doc.incentive_amount = flt(incentive_amount)
            doc.incentive_days = incentive_days

            doc.insert(ignore_permissions=True)
            doc.submit()

            created_incentives.append(doc.name)

        except Exception as e:
            frappe.log_error(f"Error processing {emp}: {str(e)}", "Employee Incentive Batch")

    return {
        "status": "success",
        "total_created": len(created_incentives),
        "incentives": created_incentives
    }

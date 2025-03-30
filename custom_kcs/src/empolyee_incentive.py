import frappe
from frappe.utils import flt

@frappe.whitelist()
def calculate_incentive_for_employee(employee, start_date):
    if not start_date:
        frappe.throw("Missing start_date!")

    end_date = get_last_day(start_date)

    employee_data = frappe.get_value(
        "Employee", {"name": employee}, ["branch", "shift"], as_dict=True
    )
    if not employee_data:
        frappe.throw(f"Employee {employee} not found!")

    assigned_branch = employee_data["branch"]
    assigned_shift = employee_data["shift"]

    attendance_records = frappe.get_all(
        "Attendance",
        filters={"employee": employee, "attendance_date": ["between", [start_date, end_date]]},
        fields=["attendance_date", "branch", "shift", "status"]
    )

    incentive_days = 0
    total_incentive_salary = 0

    for att in attendance_records:
        if att["status"] != "Absent" and (att["branch"] != assigned_branch or att["shift"] != assigned_shift):
            incentive_days += 1
            total_incentive_salary += calculate_incentive_per_day(employee, att["branch"], start_date)

    return {
        "incentive_amount": total_incentive_salary,
        "incentive_days": incentive_days
    }

def get_last_day(date_str):
    from frappe.utils import getdate, add_days
    import calendar

    date_obj = getdate(date_str)
    last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
    return add_days(date_obj.replace(day=1), last_day - 1)


def calculate_incentive_per_day(employee, branch_name, start_date):
    from frappe.utils import flt

    # Get total days in the month
    total_days_in_month = frappe.db.sql(
        """SELECT DAY(LAST_DAY(%s)) AS days""", (start_date,)
    )[0][0]

    # Get employee doc to fetch role/designation
    employee_doc = frappe.get_doc("Employee", employee)
    employee_role = employee_doc.designation  

    # Fetch branch doc and find salary structure for the employee role
    branch_doc = frappe.get_doc("Branch", branch_name)
    salary_structure = None

    for role in branch_doc.roles:
        if role.role == employee_role:
            salary_structure = role.salary_structure
            break

    if not salary_structure:
        frappe.logger().error(f"No Salary Structure found in Branch {branch_name} for role {employee_role}")
        return 0

    # Get total of all earnings from salary structure
    earnings = frappe.get_all("Salary Detail",
        filters={"parent": salary_structure, "parenttype": "Salary Structure"},
        fields=["amount"]
    )

    if not earnings:
        frappe.logger().error(f"No earnings found in Salary Structure {salary_structure}")
        return 0

    total_earning = sum(flt(e["amount"]) for e in earnings)
    incentive_per_day = total_earning / total_days_in_month

    return round(incentive_per_day, 2)


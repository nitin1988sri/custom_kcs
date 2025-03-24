import frappe
from frappe.utils import flt
from frappe.utils.data import money_in_words
import json

@frappe.whitelist()
def get_employee_attendance_data(employee, start_date=None, end_date=None):
    if start_date is None or end_date is None:
        return
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

    payment_days = 0
    incentive_days = 0
    absent_days = 0
    total_incentive_salary = 0

    for att in attendance_records:
        if att["status"] == "Absent":
            absent_days += 1
        elif att["branch"] == assigned_branch and att["shift"] == assigned_shift:
            payment_days += 1
        else:
            incentive_days += 1
            total_incentive_salary += calculate_incentive_per_day(employee, att["branch"], start_date)

    base_salary = frappe.get_value("Salary Structure Assignment", {"employee": employee}, "base") or 0
    in_hand_salary = (flt(base_salary) / 26) * payment_days if base_salary else 0

    gross_pay = in_hand_salary + total_incentive_salary
    rounded_gross_pay = round(gross_pay) - 0
    total_in_words = money_in_words(rounded_gross_pay, "INR")

    return {
        "payment_days": payment_days,
        "absent_days": absent_days,
        "incentive_days": incentive_days,
        "in_hand_salary": in_hand_salary,
        "incentive_salary": total_incentive_salary,
        "gross_pay": gross_pay,
        "rounded_gross_pay": rounded_gross_pay,
        "total_in_words": total_in_words
    }

def calculate_incentive_per_day(employee, branch, start_date):
    total_days_in_month = frappe.db.sql(
        """SELECT DAY(LAST_DAY(%s)) AS days""", (start_date,)
    )[0][0]

    employee = frappe.get_doc("Employee", employee)
    employee_role = employee.designation  

    contract = frappe.get_value("Contract", {"branch": branch, "docstatus": 1}, ["name"], as_dict=True)
    if not contract:
        frappe.logger().error(f"No active contract found for branch {branch}")
        return 0

    contract_name = contract["name"]

    contract_role = frappe.get_value(
        "Contract Role",
        {"parent": contract_name, "role": employee_role},
        ["salary_structure"],
        as_dict=True
    )

    if not contract_role or not contract_role["salary_structure"]:
        frappe.logger().error(f"No billing rate found for {employee_role} in {contract_name}")
        return 0


    salary_structure = contract_role["salary_structure"]
    earnings = frappe.get_all("Salary Detail",
                              filters={"parent": salary_structure, "salary_component": "In Hand"},
                              fields=["amount"])

    if not earnings:
        frappe.logger().error(f"No 'In Hand' salary found in Salary Structure {salary_structure}")
        return 0

    in_hand_per_month = flt(earnings[0]["amount"])
    incentive_per_day = in_hand_per_month / total_days_in_month  

    return incentive_per_day


@frappe.whitelist()
def get_employee_attendance_data_on_save(doc, method):
    
    frappe.log_error(f"Processing Salary Slip for {doc.employee} from {doc.start_date} to {doc.end_date}", "Debugging Salary Slip")

    if not doc.start_date or not doc.end_date:
        frappe.throw("Missing start_date or end_date in Salary Slip!")

    employee_data = frappe.get_value(
        "Employee", {"name": doc.employee}, ["branch", "shift"], as_dict=True
    )
    if not employee_data:
        frappe.throw(f"Employee {doc.employee} not found!")

    assigned_branch = employee_data["branch"]
    assigned_shift = employee_data["shift"]

    attendance_records = frappe.get_all(
        "Attendance",
        filters={"employee": doc.employee, "attendance_date": ["between", [doc.start_date, doc.end_date]]},
        fields=["attendance_date", "branch", "shift", "status"]
    )

    payment_days = 0
    incentive_days = 0
    absent_days = 0
    total_incentive_salary = 0

    for att in attendance_records:
        if att["status"] == "Absent":
            absent_days += 1
        elif att["branch"] == assigned_branch and att["shift"] == assigned_shift:
            payment_days += 1
        else:
            incentive_days += 1
            total_incentive_salary += calculate_incentive_per_day(doc.employee, att["branch"], doc.start_date)

    base_salary = frappe.get_value("Salary Structure Assignment", {"employee": doc.employee}, "base") or 0
    in_hand_salary = (flt(base_salary) / 26) * payment_days if base_salary else 0

    gross_pay = in_hand_salary + total_incentive_salary
    rounded_gross_pay = round(gross_pay)-0
    total_in_words = money_in_words(rounded_gross_pay, "INR")

    frappe.log_error(f"Final Salary Calculation - Employee: {doc.employee}, Payment Days: {payment_days}, Gross Pay: {gross_pay}, Incentive: {total_incentive_salary}", "Salary Debug")

    doc.earnings = []
    doc.append("earnings", {
        "salary_component": "In Hand",
        "amount": in_hand_salary,
        "depends_on_payment_days": 0 
    })
    doc.append("earnings", {
        "salary_component": "Incentive",
        "amount": total_incentive_salary
    })

    doc.payment_days = payment_days
    doc.absent_days = absent_days
    doc.incentive_days = incentive_days
    doc.gross_pay = gross_pay
    doc.rounded_total = rounded_gross_pay
    doc.total_in_words = total_in_words
    doc.net_pay = rounded_gross_pay - 0
    earnings_list = [earning.as_dict() for earning in doc.earnings]
    earnings_str = json.dumps(earnings_list, indent=2)

    frappe.log_error("Updated Salary Slip successfully", "Salary Debug")

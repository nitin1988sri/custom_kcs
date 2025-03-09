import frappe
from frappe.utils import flt
from frappe.utils.data import money_in_words

@frappe.whitelist()
def get_employee_attendance_data(employee, start_date, end_date):

    """
    Fetch Payment Days, Incentive Days, and Absent Days based on Attendance.
    Calculate In-Hand, Incentive, and Gross Pay dynamically.
    """

    # Fetch assigned branch & shift from Employee Doctype
    employee_data = frappe.get_value(
        "Employee", {"name": employee}, ["branch", "shift"], as_dict=True
    )

    if not employee_data:
        frappe.throw(f"Employee {employee} not found!")

    assigned_branch = employee_data["branch"]
    assigned_shift = employee_data["shift"]

    # Fetch attendance records
    attendance_records = frappe.get_all(
        "Attendance",
        filters={"employee": employee, "attendance_date": ["between", [start_date, end_date]]},
        fields=["attendance_date", "branch", "shift", "status"]
    )

    # Initialize counts
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
            # Incentive Calculation for different branch/shift
            incentive_days += 1
            total_incentive_salary += calculate_incentive_per_day(employee, att["branch"], start_date, end_date)

    # Fetch Base Salary
    base_salary = frappe.get_value("Salary Structure Assignment", {"employee": employee}, "base") or 0
    in_hand_salary = (flt(base_salary) / 26) * payment_days if base_salary else 0

    # **Calculate Gross Pay**
    gross_pay = in_hand_salary + total_incentive_salary
    rounded_gross_pay = round(gross_pay)
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


def calculate_incentive_per_day(employee, branch, start_date, end_date):
    """
    Calculate the incentive salary for a single day based on contract billing rate.
    """

    # Find the active contract for this branch
    contract = frappe.get_value("Contract", {"branch": branch, "docstatus": 1}, ["name"], as_dict=True)
    if not contract:
        frappe.logger().error(f"No active contract found for branch {branch}")
        return 0

    contract_name = contract["name"]

    # Fetch employee's role and billing rate from contract
    contract_role = frappe.get_value(
        "Contract Role",
        {"parent": contract_name, "role": "Security guard"},
        ["billing_rate", "employee_percent"],
        as_dict=True
    )

    if not contract_role or not contract_role["billing_rate"] or not contract_role["employee_percent"]:
        frappe.logger().error(f"No billing rate found for Security Guard in {contract_name}")
        return 0

    billing_rate = flt(contract_role["billing_rate"])
    employee_percent = flt(contract_role["employee_percent"]) / 100  # Convert to decimal

    # Fetch total days in the salary month
    total_days_in_month = frappe.db.sql(
        """SELECT DAY(LAST_DAY(%s)) AS days""", (start_date)
    )[0][0]

    # Calculate incentive per day
    incentive_per_day = (billing_rate * employee_percent) / total_days_in_month
    return incentive_per_day


@frappe.whitelist()
def get_employee_attendance_data_on_save(doc, method):
    """
    Fetch Payment Days, Incentive Days, and Absent Days based on Attendance.
    Calculate In-Hand, Incentive, and Gross Pay dynamically before saving Salary Slip.
    """

    frappe.log_error(f"Processing Salary Slip for {doc.employee} from {doc.start_date} to {doc.end_date}", "Debugging Salary Slip")

    if not doc.start_date or not doc.end_date:
        frappe.throw("Missing start_date or end_date in Salary Slip!")

    # Fetch assigned branch & shift from Employee Doctype
    employee_data = frappe.get_value(
        "Employee", {"name": doc.employee}, ["branch", "shift"], as_dict=True
    )

    if not employee_data:
        frappe.throw(f"Employee {doc.employee} not found!")

    assigned_branch = employee_data["branch"]
    assigned_shift = employee_data["shift"]

    # Fetch attendance records
    attendance_records = frappe.get_all(
        "Attendance",
        filters={"employee": doc.employee, "attendance_date": ["between", [doc.start_date, doc.end_date]]},
        fields=["attendance_date", "branch", "shift", "status"]
    )

    # Initialize counts
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
            # Incentive Calculation for different branch/shift
            incentive_days += 1
            total_incentive_salary += calculate_incentive_per_day(doc.employee, att["branch"], doc.start_date, doc.end_date)

    # Fetch Base Salary
    base_salary = frappe.get_value("Salary Structure Assignment", {"employee": doc.employee}, "base") or 0
    in_hand_salary = (flt(base_salary) / 26) * payment_days if base_salary else 0

    # **Calculate Gross Pay**
    gross_pay = in_hand_salary + total_incentive_salary
    rounded_gross_pay = round(gross_pay)
    total_in_words = money_in_words(rounded_gross_pay, "INR")

    # Assign values back to doc
    doc.payment_days = payment_days
    doc.absent_days = absent_days
    doc.incentive_days = incentive_days
    doc.gross_pay = gross_pay
    doc.rounded_total = rounded_gross_pay
    doc.total_in_words = total_in_words

    frappe.log_error(f"Final Salary Calculation - Employee: {doc.employee}, Gross Pay: {gross_pay}, Incentive: {total_incentive_salary}", "Salary Debug")


def calculate_incentive_per_day(employee, branch, start_date, end_date):
    """
    Calculate the incentive salary for a single day based on contract billing rate.
    """

    # Find the active contract for this branch
    contract = frappe.get_value("Contract", {"branch": branch, "docstatus": 1}, ["name"], as_dict=True)
    if not contract:
        frappe.logger().error(f"No active contract found for branch {branch}")
        return 0

    contract_name = contract["name"]

    # Fetch employee's role and billing rate from contract
    contract_role = frappe.get_value(
        "Contract Role",
        {"parent": contract_name, "role": "Security guard"},
        ["billing_rate", "employee_percent"],
        as_dict=True
    )

    if not contract_role or not contract_role["billing_rate"] or not contract_role["employee_percent"]:
        frappe.logger().error(f"No billing rate found for Security Guard in {contract_name}")
        return 0

    billing_rate = flt(contract_role["billing_rate"])
    employee_percent = flt(contract_role["employee_percent"]) / 100  # Convert to decimal

    # Fetch total days in the salary month
    total_days_in_month = frappe.db.sql(
        """SELECT DAY(LAST_DAY(%s)) AS days""", (start_date)
    )[0][0]

    # Calculate incentive per day
    incentive_per_day = (billing_rate * employee_percent) / total_days_in_month
    return incentive_per_day

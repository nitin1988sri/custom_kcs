import frappe
from frappe.utils import get_first_day, get_last_day, flt

@frappe.whitelist()
def calculate_payment_and_incentive_days(employee_id, month, year):
 
    start_date = get_first_day(f"{year}-{month}-01")
    end_date = get_last_day(f"{year}-{month}-01")

    employee = frappe.get_doc("Employee", employee_id)
    employee_role = employee.designation  

    check_ins = frappe.get_all("Employee Checkin",
                               filters={"employee": employee_id, "time": ["between", [start_date, end_date]]},
                               fields=["time", "branch"])

    contracts = frappe.get_all("Contract",
                               filters={"branch": ["in", [check["branch"] for check in check_ins]]},
                               fields=["name", "branch"],
                               order_by="modified desc")

    contract_map = {}

    for contract in contracts:
        contract_roles = frappe.get_all("Contract Role",
                                        filters={"parent": contract["name"], "role": employee_role},
                                        fields=["billing_rate", "employee_percent"])

        if contract_roles:
            contract_map[contract["branch"]] = {
                "billing_rate": flt(contract_roles[0]["billing_rate"]),
                "employee_percent": flt(contract_roles[0]["employee_percent"])
            }

    work_days = {}
    for check in check_ins:
        checkin_date = check["time"].date()
        branch = check["branch"]

        if checkin_date not in work_days:
            work_days[checkin_date] = {}

        if branch not in work_days[checkin_date]:
            work_days[checkin_date][branch] = 0

        work_days[checkin_date][branch] += 1  # Counting number of shifts in a day per branch

    incentive_salary = 0
    total_incentive_days = 0

    # Calculate incentive salary
    for date, branches in work_days.items():
        incentive_counted_for_day = False  # Ensure incentive is counted only once per branch per day

        for branch, shifts in branches.items():
            if branch not in contract_map:
                continue  # Skip if branch has no contract

            billing_rate = contract_map[branch]["billing_rate"]
            employee_percent = contract_map[branch]["employee_percent"]
            per_shift_incentive = (billing_rate * employee_percent) / (100 * 30)

            if shifts >= 2 and not incentive_counted_for_day:
                total_incentive_days += 1
                incentive_salary += per_shift_incentive
                incentive_counted_for_day = True

    return {
        "employee": employee_id,
        "month": month,
        "year": year,
        "total_incentive_days": total_incentive_days,
        "incentive_salary": round(incentive_salary, 2)
    }

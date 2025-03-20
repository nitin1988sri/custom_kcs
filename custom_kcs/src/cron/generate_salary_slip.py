import frappe
from frappe.utils import get_first_day, get_last_day, flt
from datetime import datetime

@frappe.whitelist()
def generate_salary_slip(emp_id=None, month=None, year=None):
    now = datetime.today()
    month = month or now.month
    year = year or now.year

    start_date = get_first_day(f"{year}-{month}-01")
    end_date = get_last_day(f"{year}-{month}-01")

    filters = {"status": "Active"}
    if emp_id:
        filters["name"] = emp_id  

    employees = frappe.get_all("Employee", filters=filters, fields=["name", "company"])

    if not employees:
        print("No active employees found!")
        return

    for emp in employees:
        in_hand_salary, salary_structure = get_in_hand_salary(emp["name"], start_date)
        salary_data = calculate_payment_and_incentive_days(emp["name"], month, year, in_hand_salary)

        if frappe.db.exists("Salary Slip", {"employee": emp["name"], "start_date": start_date, "end_date": end_date}):
            print(f"Salary Slip already exists for {emp['name']} in {month}-{year}, skipping.")
            continue

        salary_slip = frappe.get_doc({
            "doctype": "Salary Slip",
            "employee": emp["name"],
            "start_date": start_date,
            "end_date": end_date,
            "company": emp["company"],
            "payroll_frequency": "Monthly",
            "payment_days": salary_data["total_payment_days"],
            "absent_days": salary_data["absent_days"],
            "incentive_days": salary_data["total_incentive_days"],
            "earnings": [
                {"salary_component": "In Hand", "amount": flt(salary_data["in_hand_salary"])},  
                {"salary_component": "Incentive", "amount": flt(salary_data["incentive_salary"])}
            ],
            "gross_pay": flt(salary_data["gross_pay"]),
            "net_pay": flt(salary_data["rounded_gross_pay"]),
            "salary_structure": salary_structure
        })

        salary_slip.insert(ignore_permissions=True)
        salary_slip.submit()

    frappe.db.commit()
    print("All Salary Slips Generated Successfully!")

def get_in_hand_salary(employee_id, start_date):

    assignment = frappe.db.sql("""
                                    SELECT salary_structure 
                                    FROM `tabSalary Structure Assignment`
                                    WHERE employee = %s AND from_date <= %s
                                    ORDER BY from_date DESC LIMIT 1
                                """, (employee_id, start_date), as_dict=True)

    if not assignment:
        frappe.throw(f" No valid Salary Structure assigned for {employee_id} applicable before {start_date}")

    salary_structure = assignment[0]["salary_structure"]

    earnings = frappe.get_all("Salary Detail",
                              filters={"parent": salary_structure, "salary_component": "In Hand"},
                              fields=["amount"])

    in_hand_salary = flt(earnings[0]["amount"]) if earnings else 10000  

    return in_hand_salary, salary_structure  

def calculate_payment_and_incentive_days(employee_id, month, year, in_hand_salary):
    start_date = get_first_day(f"{year}-{month}-01")
    end_date = get_last_day(f"{year}-{month}-01")
    total_days_in_month = end_date.day  

    employee = frappe.get_doc("Employee", employee_id)
    assigned_branch = employee.branch  
    assigned_shift = employee.shift
    employee_role = employee.designation  

    check_ins = frappe.get_all("Attendance",
                               filters={"employee": employee_id, "attendance_date": ["between", [start_date, end_date]]},
                               fields=["attendance_date", "shift", "branch", "status"])

    contracts = frappe.get_all("Contract",
                               filters={"branch": ["in", [check["branch"] for check in check_ins]]},
                               fields=["name", "branch"],
                               order_by="modified desc")

    contract_map = {}
    for contract in contracts:
        contract_roles = frappe.get_all("Contract Role",
                                        filters={"parent": contract["name"], "role": employee_role},
                                        fields=["billing_rate", "salary_structure"])
        
        for role in contract_roles:
            salary_structure = role["salary_structure"]
            earnings = frappe.get_all("Salary Detail",
                                      filters={"parent": salary_structure, "salary_component": "In Hand"},
                                      fields=["amount"])
           
            if earnings:
                in_hand_per_month = flt(earnings[0]["amount"])
                daily_salary = in_hand_per_month / total_days_in_month 
                
                contract_map[contract["branch"]] = {
                    "daily_salary": daily_salary
                }

    work_days = {}  
    incentive_days = 0  
    absent_days = 0
    incentive_salary = 0  

    for check in check_ins:
        checkin_date = check["attendance_date"]
        branch = check["branch"]
        shift = check["shift"]

        if check["status"] == "Absent":
            absent_days += 1
            continue

        if branch == assigned_branch and shift == assigned_shift:
            if checkin_date not in work_days:
                work_days[checkin_date] = {"shifts": 1}
            else:
                work_days[checkin_date]["shifts"] += 1
        else:
            incentive_days += 1
            if branch in contract_map:
                incentive_salary += contract_map[branch]["daily_salary"]

    total_payment_days = len(work_days.keys())  
    absent_days = total_days_in_month - total_payment_days  

    daily_in_hand_salary = in_hand_salary / total_days_in_month
    absent_deduction = daily_in_hand_salary * absent_days
    final_in_hand_salary = in_hand_salary - absent_deduction  

    gross_pay = final_in_hand_salary + incentive_salary
    rounded_gross_pay = round(gross_pay, 2)
    return {
        "employee": employee_id,
        "month": month,
        "year": year,
        "total_payment_days": total_payment_days,
        "absent_days": absent_days,
        "total_incentive_days": incentive_days,
        "incentive_salary": round(incentive_salary, 2),
        "in_hand_salary": round(final_in_hand_salary, 2),  
        "gross_pay": gross_pay,
        "rounded_gross_pay": rounded_gross_pay
    }

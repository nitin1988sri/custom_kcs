import frappe
import random
from datetime import datetime, timedelta

def get_random_client():
    clients = frappe.get_all("Client", fields=["name"])
    return random.choice(clients)["name"] if clients else None

def get_random_branch(client):
    branches = frappe.get_all("Branch", filters={"client": client}, fields=["name"])
    return random.choice(branches)["name"] if branches else None

def get_day_shift():
    shift = frappe.get_value("Shift", {"shift_name": "Day Shift"}, "name")
    return shift

def create_users_and_employees():
    employee_ids = []
    
    for i in range(1, 2):
        first_name = f"Employee{i}"
        email = f"employee{i}@example.com"
        gender = random.choice(["Male", "Female"])
        date_of_birth = (datetime.today() - timedelta(days=random.randint(8000, 15000))).strftime("%Y-%m-%d")  # Random DOB
        date_of_joining = frappe.utils.today()
        
        client = get_random_client()
        if not client:
            print("❌ No Client found! Skipping Employee creation.")
            continue
        
        branch = get_random_branch(client)
        if not branch:
            print(f"❌ No Branch found for Client {client}! Skipping Employee creation.")
            continue
        
        shift = get_day_shift()
        if not shift:
            print("❌ 'Day Shift' not found! Skipping Employee creation.")
            continue

        if not frappe.db.exists("User", email):
            user = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": first_name,
                "send_welcome_email": 0,
                "roles": [{"role": "Employee"}]
            })
            user.insert(ignore_permissions=True)
            print(f"✅ User Created: {email}")

        if not frappe.db.exists("Employee", {"user_id": email}):
            employee = frappe.get_doc({
                "doctype": "Employee",
                "employee_name": first_name,
                "first_name": first_name,
                "gender": gender,
                "date_of_birth": date_of_birth,
                "date_of_joining": date_of_joining,
                "user_id": email,
                "status": "Active",
                "company": "Your Company Name",
                "client": client,
                "branch": branch,
                "shift": shift,
                "employee_number": f"EMP00{i}"
            })
            employee.insert(ignore_permissions=True)
            employee_ids.append(employee.name)
            print(f"✅ Employee Created: {first_name}, Client: {client}, Branch: {branch}, Shift: {shift}")

    return employee_ids


def mark_attendance(employee_ids):
    for emp in employee_ids:
        if not frappe.db.exists("Attendance", {"employee": emp, "attendance_date": frappe.utils.today()}):
            attendance = frappe.get_doc({
                "doctype": "Attendance",
                "employee": emp,
                "attendance_date": frappe.utils.today(),
                "status": "Present",
                "company": "Your Company Name"
            })
            attendance.insert(ignore_permissions=True)
            print(f"✅ Attendance Marked: {emp}")

def generate_salary_slip(employee_ids):
    for emp in employee_ids:
        basic_salary = random.randint(20000, 50000)
        
        if not frappe.db.exists("Salary Slip", {"employee": emp, "start_date": "2025-03-01", "end_date": "2025-03-31"}):
            salary_slip = frappe.get_doc({
                "doctype": "Salary Slip",
                "employee": emp,
                "start_date": "2025-03-01",
                "end_date": "2025-03-31",
                "company": "Your Company Name",
                "payroll_frequency": "Monthly",
                "earnings": [{"salary_component": "Basic", "amount": basic_salary}],
                "gross_pay": basic_salary,
                "net_pay": basic_salary
            })
            salary_slip.insert(ignore_permissions=True)
            print(f"✅ Salary Slip Created: {emp} - ₹{basic_salary}")

def main():
    create_users_and_employees()
   
main()

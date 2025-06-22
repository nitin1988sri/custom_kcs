import csv
import frappe
import random
from frappe.utils import getdate

def sanitize(value, default):
    if not value or value.strip() in ("#FMT", "###", "nan", "NaN"):
        return default
    return value.strip()

def create_user_if_not_exists(name, email):
    user_id = email if email and email.strip() else f"{name.replace(' ', '').lower()}@example.com"
    if not frappe.db.exists("User", user_id):
        doc = frappe.get_doc({
            "doctype": "User",
            "email": user_id,
            "first_name": name.strip().title(),
            "send_welcome_email": 0
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Created User: {user_id}")
    else:
        print(f"ℹ️ User already exists: {user_id}")
    return user_id

def create_designation_if_not_exists(designation):
    if not frappe.db.exists("Designation", designation):
        doc = frappe.get_doc({
            "doctype": "Designation",
            "designation_name": designation
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"🎯 Created Designation: {designation}")
    return designation

def create_employee(row):
    emp_id = row.get("Emp Id", "").strip()
    name = row.get("Name", "").strip()
    email = sanitize(row.get("Email", ""), f"{emp_id.lower()}@example.com")
    phone = sanitize(row.get("Phone", ""), str(random.randint(7000000000, 9999999999)))
    dob = getdate(row.get("DOB", "1990-01-01"))
    doj = getdate(row.get("DOJ", "2024-01-01"))
    aadhar = sanitize(row.get("AADHAR", ""), frappe.generate_hash(length=12))
    pan = sanitize(row.get("PAN", ""), "AAAAA0000A")
    uan = sanitize(row.get("UAN", ""), "0")
    esic = sanitize(row.get("ESIC", ""), "0")
    designation = sanitize(row.get("Deg.", ""), "Field Officer")

    user_id = create_user_if_not_exists(name, email)
    designation = create_designation_if_not_exists(designation)

    if frappe.db.exists("Employee", emp_id):
        print(f"👨‍💼 Employee already exists: {emp_id}")
        return

    first_name = name.split()[0]
    last_name = name.split()[-1] if len(name.split()) > 1 else ""

    doc = frappe.get_doc({
        "doctype": "Employee",
        "name": emp_id,
        "employee_name": name,
        "employee_number": emp_id,
        "user_id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "date_of_birth": dob,
        "date_of_joining": doj,
        "gender": "Male",
        "client": "KCS internal",
        "branch": "KCS internal branch",
        "status": "Active",
        "designation": designation,
        "aadhaar_number": aadhar,
        "esic_number": esic,
        "uan": uan,
        "cell_number": phone,
        "pan_number": pan,
        "employment_type": "Full-time",
        "department": "Operations",
        "shift": "Day Shift",
        "grade": "A",
    })

    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"✅ Created Employee: {emp_id} - {name}")

def cleanup_previous_data():
    import os

    csv_path = frappe.get_site_path("public", "files", "internal_emp.csv")
    if not os.path.exists(csv_path):
        print("❌ CSV file not found at:", csv_path)
        return

    deleted_users, deleted_emps = [], []

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            emp_id = row.get("Emp Id", "").strip()
            email = sanitize(row.get("Email", ""), f"{emp_id.lower()}@example.com")
            name = row.get("Name", "").strip()
            user_id = email if email.strip() else f"{name.replace(' ', '').lower()}@example.com"

            # Delete Employee
            if frappe.db.exists("Employee", emp_id):
                try:
                    frappe.delete_doc("Employee", emp_id, force=True)
                    deleted_emps.append(emp_id)
                except Exception as e:
                    print(f"❌ Failed to delete Employee {emp_id}: {e}")

            # Delete User
            if frappe.db.exists("User", user_id):
                try:
                    frappe.delete_doc("User", user_id, force=True)
                    deleted_users.append(user_id)
                except Exception as e:
                    print(f"❌ Failed to delete User {user_id}: {e}")

    frappe.db.commit()
    print(f"🧹 Deleted Employees: {deleted_emps}")
    print(f"🧹 Deleted Users: {deleted_users}")

def run():
    csv_path = frappe.get_site_path("public", "files", "internal_emp.csv")
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                create_employee(row)
            except Exception as e:
                print(f"❌ Error while processing {row.get('Emp Id')}: {str(e)}")

def full_import():
    cleanup_previous_data()
    run()

import csv
import frappe
from frappe.utils import getdate
from frappe.core.doctype.user import user

frappe.local.conf.rate_limit = False
user.throttle_user_creation = lambda: None

def create_user_if_not_exists(user_name, email=None):
    user_id = email if email else f"{user_name.replace(' ', '').lower()}@example.com"
    if not frappe.db.exists("User", user_id):
        doc = frappe.get_doc({
            "doctype": "User",
            "email": user_id,
            "first_name": user_name.strip().title(),
            "send_welcome_email": 0
        })
        doc.flags.ignore_permissions = True
        doc.flags.ignore_email_queue = True
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
    return user_id

def parse_name(full_name):
    parts = full_name.strip().split()
    first = parts[0] if len(parts) > 0 else "First"
    middle = parts[1] if len(parts) > 2 else ""
    last = parts[-1] if len(parts) > 1 else "Last"
    return first, middle, last

def create_dummy_employee(emp_name, branch_name, user_id):
    if frappe.db.exists("Employee", {"employee_name": emp_name}):
        return frappe.db.get_value("Employee", {"employee_name": emp_name}, "name")

    first_name, middle_name, last_name = parse_name(emp_name)
    doc = frappe.get_doc({
        "doctype": "Employee",
        "employee_number": frappe.generate_hash(length=8),
        "employee_name": emp_name,
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "date_of_birth": getdate("1990-01-01"),
        "date_of_joining": getdate("2024-01-01"),
        "branch": branch_name,
        "designation": "Security Guard",
        "company": "KCS",
        "user_id": user_id,
        "status": "Active",
        "gender": "Male",
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.name

def assign_branch_manager(employee_name, branch_name):
    try:
        branch_doc = frappe.get_doc("Branch", branch_name)
        branch_doc.branch_manager = employee_name
        branch_doc.save(ignore_permissions=True)
        frappe.db.commit()
        print(f"🔗 Assigned {employee_name} as manager to branch: {branch_name}")
    except Exception as e:
        print(f"❌ Failed to assign manager for branch {branch_name}: {str(e)}")

def run():
    csv_path = frappe.get_site_path("public", "files", "epm-branch.csv")
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                emp_name = row["EMPLOYEENAME"].strip()
                branch_name = row["UNITNAME"].strip()

                user_id = create_user_if_not_exists(emp_name)
                employee_docname = create_dummy_employee(emp_name, branch_name, user_id)

                assign_branch_manager(employee_docname, branch_name)
                print(f"✅ Done: {emp_name} -> {branch_name}")

            except Exception as e:
                print(f"❌ Error for {row}: {str(e)}")

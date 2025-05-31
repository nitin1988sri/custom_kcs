import csv
import os
import frappe
frappe.local.conf.rate_limit = False
from frappe.utils import getdate

from frappe.core.doctype.user import user

def skip_throttle(): pass
user.throttle_user_creation = skip_throttle


def create_state_if_not_exists(country_name, state_name):
    state_name = state_name.strip().title()
    country_name = country_name.strip().title()

    if not frappe.db.exists("State", {"state_name": state_name}):
        try:
            doc = frappe.get_doc({
                "doctype": "State",
                "state_name": state_name,
                "country": country_name
            })
            doc.insert()
            frappe.db.commit()
        except frappe.DuplicateEntryError:
            print(f"⚠️ State '{state_name}' already exists, skipping insert.")
        except Exception as e:
            print(f"❌ Failed to insert state '{state_name}': {e}")

    return frappe.get_value("State", {"state_name": state_name}, "name")

def create_city_if_not_exists(state_name, city_name):
    city_name = city_name.strip().title()

    if not frappe.db.exists("City", {"city_name": city_name}):
        try:
            doc = frappe.get_doc({
                "doctype": "City",
                "city_name": city_name,
                "state": state_name
            })
            doc.insert()
            frappe.db.commit()
        except frappe.DuplicateEntryError:
            print(f"⚠️ City '{city_name}' already exists, skipping insert.")

    return frappe.get_value("City", {"city_name": city_name}, "name")

def create_client_if_not_exists(client_name):
    if not frappe.db.exists("Customer", client_name):
        doc = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": client_name.strip().title(),
            "customer_type": "Company",
            "customer_group": "Commercial",
            "territory": "India"
        })
        doc.insert()
        frappe.db.commit()
    return client_name

def create_branch_if_not_exists(row, client_name, city, state, branch_manager=None):
    branch_name = row["UNITNAME"].strip().title()
    if not frappe.db.exists("Branch", {"branch_name": branch_name}):
        doc = frappe.get_doc({
            "doctype": "Branch",
            "branch_name": branch_name,
            "client": client_name.strip().title(),
            "city": city,
            "state": state,
            "contact_name": 'NA',
            "contact_phone": row.get("Phone", "9999999999"),
            "branch_manager": branch_manager,
            "contact_email": row.get("Email", ""),
            "gst": row.get("GST", ""),
            "billing_location": row.get("Billing Location", ""),
            "address": row.get("Service Location", ""),
            "old_branch_code": row.get("UNITCODE", ""),
            "status": "Active",
            "grade": row.get("Grade", "D")
        })
        doc.insert()
        frappe.db.commit()
    return frappe.get_value("Branch", {"branch_name": branch_name}, "name")

def create_user_if_not_exists(userName, email=None):
    user_id = email if email else f"{userName}@gmail.com"
    if not frappe.db.exists("User", user_id):
        doc = frappe.get_doc({
            "doctype": "User",
            "email": user_id,
            "first_name": userName.strip().title(),
            "send_welcome_email": 0
        })
        doc.flags.ignore_permissions = True
        doc.flags.ignore_email_queue = True
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
    return user_id

def create_employee(row, branch_name, user_id):
    emp_code = row["EMPCODE"]
    if not frappe.db.exists("Employee", {"employee_number": emp_code}):
        first_name, middle_name, last_name = parse_name(row["EMPLOYEENAME"])
        doc = frappe.get_doc({
            "doctype": "Employee",
            "old_empcode": emp_code,
            "first_name": first_name.strip().title(),
            "middle_name": middle_name.strip().title(),
            "last_name": last_name.strip().title(),
            "branch": branch_name.strip().title(),
            "date_of_birth": getdate(row["DOB"]),
            "date_of_joining": getdate(row["DOJ"]),
            "aadhaar_number": row["Aadhar"],
            "designation": get_or_create_designation(row["DESINAME"]),
            "father_name": row["FATHERNAME"],
            "uan_number": row["UANNUMBER"],
            "esic_number": row["ESINO"],
            "user_id": user_id,
            "status": "Active",
            "company": "KCS",
            "grade": row.get("Grade", "D"),
            "department": row.get("Department", "General"),
            "employment_type": row.get("Employment Type", "Full-time"),
            "shift": row.get("Shift", "Day Shift"),
            "client": row["CUSTOMER NAME"],
            "branch": row["UNITNAME"],
            "gender": "Male",
        })
        doc.insert()
        frappe.db.commit()

def parse_name(full_name):
    parts = full_name.strip().split()
    first = parts[0] if len(parts) > 0 else ""
    middle = parts[1] if len(parts) > 2 else ""
    last = parts[-1] if len(parts) > 1 else ""
    return first, middle, last

def get_or_create_designation(name):
    if not frappe.db.exists("Designation", {"designation_name": name}):
        doc = frappe.get_doc({
            "doctype": "Designation",
            "designation_name": name.strip().title()
        })
        doc.insert()
        frappe.db.commit()
    return name


def truncateDataFirst():

    tables = [
        "tabCity",
        "tabState",
        "tabEmployee",
        "tabBranch",
        "tabCustomer"
    ]

    for table in tables:
        try:
            frappe.db.sql_ddl(f"TRUNCATE `{table}`")
            print(f"✅ Truncated {table}")
        except Exception as e:
            print(f"❌ Error truncating {table}: {str(e)}")


def run():
    #truncateDataFirst()
    from frappe.core.doctype.user import user
    user.throttle_user_creation = lambda: None
    csv_path = frappe.get_site_path("public", "files", "new_data_to_import.csv")
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            state = create_state_if_not_exists("India", row["State"])
            city = create_city_if_not_exists(state, row["City"])
            client = create_client_if_not_exists(row["CUSTOMER NAME"])
            branch = create_branch_if_not_exists(row, client, city, state)

            email = row.get("Email", "").strip()
            employee_name = f"{row['EMPCODE']}_{row['EMPLOYEENAME'].strip().replace(' ', '_')}"


            user_id = create_user_if_not_exists(employee_name, email)

            try:
                create_employee(row, branch, user_id)
                print(f"✅ Created Employee: {row['EMPLOYEENAME']} at Branch: {branch}")
            except frappe.exceptions.DuplicateEntryError as e:
                    print(f"⚠️  Skipped Employee {row['EMPLOYEENAME']} due to duplicate user: {str(e)}")
                    continue

            except Exception as e:
                print(f"❌ Error in row {row}: {str(e)}")
                continue

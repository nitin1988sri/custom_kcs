import frappe
from frappe.auth import LoginManager

@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    login_manager = LoginManager()
    login_manager.authenticate(usr, pwd)
    login_manager.post_login()

    user_fields = [
        "name", "full_name", "email", "first_name", "last_name", 
        "birth_date", "gender", "time_zone", "language"
    ]
    user = frappe.db.get_value("User", usr, user_fields, as_dict=True)

    employee = frappe.get_value("Employee", {"user_id": usr}, ["name", "employee_name"], as_dict=True)

    return {
        "message": "Logged In",
        "sid": frappe.session.sid,
        "user_data": user,
        "empDetails": employee
    }

@frappe.whitelist()
def logout():
    frappe.local.login_manager.logout()
    return {"message": "Logged out successfully"}

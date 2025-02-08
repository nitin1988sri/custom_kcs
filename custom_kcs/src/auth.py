import frappe
from frappe.auth import LoginManager

@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    login_manager = LoginManager()
    login_manager.authenticate(usr, pwd)
    login_manager.post_login()

    user = frappe.get_doc("User", usr)
    employee = frappe.get_value("Employee", {"user_id": user.name},  ["name", "employee_name"], as_dict=True)

    return {
        "message": "Logged In",
        "sid": frappe.session.sid,
        "full_name": user.full_name,
        "email": user.email,
        "empDetails": employee
    }

@frappe.whitelist()
def logout():
    frappe.local.login_manager.logout()
    return {"message": "Logged out successfully"}



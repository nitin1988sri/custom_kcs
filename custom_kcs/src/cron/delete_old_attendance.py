import frappe
import os
from frappe.utils import get_files_path, now_datetime, add_days

def delete_old_attendance_files():
    seven_days_ago = add_days(now_datetime(), -45)
    checkins = frappe.get_all(
        "Employee Checkin",
        filters={"creation": ("<=", seven_days_ago), "employee_image": ["!=", ""]},
        fields=["name", "employee_image", "creation"]
    )
    if not checkins:
        frappe.log_error("Attendance Cleanup", "No records found for cleanup.")
        return
    folder_path = os.path.join(get_files_path(), "attendance")
    deleted_files = []

    for checkin in checkins:
        file_url = checkin["employee_image"]
        if file_url:
            file_name = os.path.basename(file_url)
            file_path = os.path.join(folder_path, file_name)

            frappe.db.set_value("Employee Checkin", checkin["name"], "employee_image", None)
            frappe.db.commit()

            if os.path.exists(file_path):
                os.remove(file_path)
                deleted_files.append(file_name)

    frappe.log_error("Attendance Cleanup", f"Updated {len(checkins)} records & Deleted {len(deleted_files)} files: {deleted_files}")


# import frappe
# import os
# import time
# from frappe.utils import get_files_path

# def delete_old_attendance_files():
#     folder_path = os.path.join(get_files_path(), "attendance")  
#     if not os.path.exists(folder_path):
#         frappe.log_error("Attendance Cleanup", f"Folder {folder_path} does not exist.")
#         return

#     current_time = time.time()
#     retention_period = 7 * 24 * 60 * 60 
#     deleted_files = []

#     for filename in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, filename)
#         if os.path.isfile(file_path):
#             file_age = current_time - os.path.getmtime(file_path)
#             if file_age > retention_period:
#                 os.remove(file_path)
#                 deleted_files.append(filename)

#     frappe.log_error("Attendance Cleanup", f"Deleted {len(deleted_files)} files: {deleted_files}")

import frappe
import os
from frappe.utils import get_files_path, now_datetime, add_days

def delete_old_attendance_files():
    seven_days_ago = add_days(now_datetime(), -7)
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


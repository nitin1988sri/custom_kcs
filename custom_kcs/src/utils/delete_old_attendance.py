import frappe
import os
import time
from frappe.utils import get_files_path

def delete_old_attendance_files():
    folder_path = os.path.join(get_files_path(), "attendance")  
    if not os.path.exists(folder_path):
        frappe.log_error("Attendance Cleanup", f"Folder {folder_path} does not exist.")
        return

    current_time = time.time()
    retention_period = 7 * 24 * 60 * 60 
    deleted_files = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > retention_period:
                os.remove(file_path)
                deleted_files.append(filename)

    frappe.log_error("Attendance Cleanup", f"Deleted {len(deleted_files)} files: {deleted_files}")


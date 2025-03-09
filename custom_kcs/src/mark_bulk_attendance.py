import frappe
from frappe.utils import today, now, add_days
import random

def mark_bulk_attendance():
    employee_id = "HR-EMP-00002"  # Ensure only Employee ID
    company = "KCS"
    
            # Fetch all available branches dynamically from the Branch doctype
    branch_list = frappe.get_all("Branch", fields=["name"])  # Get all branch names
    branch_names = [branch["name"] for branch in branch_list]  # Extract names

    if not branch_names:
        frappe.logger().error("No branches found! Please add branches first.")
        return

    start_date = "2025-03-01"
    end_date = "2025-03-31"

    double_shift_days = random.sample(range(1, 31), 5)  # 5 days with both shifts
    absent_days = random.sample(range(1, 31), 3)  # 3 days marked as absent

    # Ensure employee exists
    employee_exists = frappe.db.get_value("Employee", {"name": employee_id}, "name")
    if not employee_exists:
        frappe.logger().error(f"Employee {employee_id} not found!")
        return

    attendance_entries = []

    for day in range(1, 40):
        attendance_date = f"2025-03-{str(day).zfill(2)}"
        random_branch = random.choice(branch_names)  # Select a random branch
        work_location = f"{random_branch} - Work Site"  # Example Work Location format

        if day in absent_days:
            try:
                attendance = frappe.get_doc({
                    "doctype": "Attendance",
                    "employee": employee_exists,
                    "attendance_date": attendance_date,
                    "status": "Absent",
                    "branch": random_branch,
                    "work_location": work_location
                })
                attendance.insert(ignore_permissions=True)
                attendance.submit()
                attendance_entries.append(attendance.name)

                frappe.logger().info(f"Marked Absent for {employee_id} on {attendance_date} (Branch: {random_branch}, Location: {work_location})")
            except Exception as e:
                frappe.logger().error(f"Failed to add attendance: {str(e)}")
        else:
            shift_status = random.choice(["Present"])
            shift = "Day shift"

            try:
                attendance = frappe.get_doc({
                    "doctype": "Attendance",
                    "employee": employee_exists,
                    "attendance_date": attendance_date,
                    "status": shift_status,
                    "shift": shift,
                    "in_time": now(),
                    "branch": random_branch,
                    "work_location": work_location
                })
                attendance.insert(ignore_permissions=True)
                attendance.submit()
                attendance_entries.append(attendance.name)

                frappe.logger().info(f"Attendance added for {employee_id} on {attendance_date} ({shift_status} - {shift}, Branch: {random_branch}, Location: {work_location})")
            except Exception as e:
                frappe.logger().error(f"Failed to add attendance: {str(e)}")

            if day in double_shift_days:
                try:
                    night_shift_status = random.choice(["Present"])
                    night_attendance = frappe.get_doc({
                        "doctype": "Attendance",
                        "employee": employee_exists,
                        "attendance_date": attendance_date,
                        "status": night_shift_status,
                        "shift": "Night shift",
                        "in_time": now(),
                        "branch": random_branch,
                        "work_location": work_location
                    })
                    night_attendance.insert(ignore_permissions=True)
                    night_attendance.submit()
                    attendance_entries.append(night_attendance.name)

                    frappe.logger().info(f"Night Shift added for {employee_id} on {attendance_date} ({night_shift_status}, Branch: {random_branch}, Location: {work_location})")
                except Exception as e:
                    frappe.logger().error(f"Failed to add night shift attendance: {str(e)}")

    # Commit only once after all insertions
    frappe.db.commit()
    frappe.logger().info(f"✅ Successfully added {len(attendance_entries)} attendance records.")

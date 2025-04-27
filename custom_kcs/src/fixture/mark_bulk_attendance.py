import frappe
from frappe.utils import today, now
import random
import calendar

def mark_bulk_attendance(month=None, year=None):
    """
    Marks attendance for all employees for the specified month and year.

    Args:
        month (int, optional): The month for which attendance should be marked (1-12). Defaults to the current month.
        year (int, optional): The year for which attendance should be marked (e.g., 2025). Defaults to the current year.
    """

    # ✅ If month and year are not provided, use the current month & year
    from datetime import datetime
    today_date = datetime.today()
    month = month or today_date.month
    year = year or today_date.year

    # ✅ Fetch all employees
    employees = frappe.get_all("Employee", fields=["name", "first_name"])
    
    if not employees:
        frappe.logger().error("❌ No employees found! Please add employees first.")
        return

    # ✅ Fetch all available branches
    branch_list = frappe.get_all("Branch", fields=["name"])  
    branch_names = [branch["name"] for branch in branch_list]  
    if not branch_names:
        frappe.logger().error("❌ No branches found! Please add branches first.")
        return

    total_days = calendar.monthrange(year, month)[1]  

    double_shift_days = random.sample(range(1, total_days + 1), 5)  
    absent_days = random.sample(range(1, total_days + 1), 3)  

    attendance_entries = []

    for employee in employees:
        employee_id = employee["name"]
        first_name = employee["first_name"]

        for day in range(1, total_days + 1): 
            attendance_date = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
            random_branch = random.choice(branch_names)  
            work_location = f"{random_branch} - Work Site"  

            if day in absent_days:
                try:
                    attendance = frappe.get_doc({
                        "doctype": "Attendance",
                        "employee": employee_id,
                        "attendance_date": attendance_date,
                        "status": "Absent",
                        "branch": random_branch
                    })
                    attendance.insert(ignore_permissions=True)
                    attendance.submit()
                    attendance_entries.append(attendance.name)

                    frappe.logger().info(f"❌ Marked Absent for {employee_id} on {attendance_date} (Branch: {random_branch})")
                except Exception as e:
                    frappe.logger().error(f"⚠ Failed to add attendance: {str(e)}")
            else:
                shift_status = "Present"
                shift = "Day shift"

                try:
                    attendance = frappe.get_doc({
                        "doctype": "Attendance",
                        "employee": employee_id,
                        "attendance_date": attendance_date,
                        "status": shift_status,
                        "shift": shift,
                        "in_time": now(),
                        "branch": random_branch
                    })
                    attendance.insert(ignore_permissions=True)
                    attendance.submit()
                    attendance_entries.append(attendance.name)

                    frappe.logger().info(f"✅ Attendance added for {employee_id} on {attendance_date} ({shift_status} - {shift}, Branch: {random_branch}, Location: {work_location})")
                except Exception as e:
                    frappe.logger().error(f"⚠ Failed to add attendance: {str(e)}")

                if day in double_shift_days:
                    try:
                        night_shift_status = "Present"
                        night_attendance = frappe.get_doc({
                            "doctype": "Attendance",
                            "employee": employee_id,
                            "attendance_date": attendance_date,
                            "status": night_shift_status,
                            "shift": "Night shift",
                            "in_time": now(),
                            "branch": random_branch
                        })
                        night_attendance.insert(ignore_permissions=True)
                        night_attendance.submit()
                        attendance_entries.append(night_attendance.name)

                        frappe.logger().info(f"🌙 Night Shift added for {employee_id} on {attendance_date} ({night_shift_status}, Branch: {random_branch}, Location: {work_location})")
                    except Exception as e:
                        frappe.logger().error(f"⚠ Failed to add night shift attendance: {str(e)}")

    frappe.db.commit()
    frappe.logger().info(f"✅ Successfully added {len(attendance_entries)} attendance records for {month}/{year}.")

# ✅ Function to support `bench execute`
def execute():
    mark_bulk_attendance(1, 2025)

import frappe
from custom_kcs.src.utils.base64_utils import decode_base64
import os
from frappe.utils import now, get_time, today

def attendance_bkp(employee, 
               status, 
               base64_image=None, 
               filename=None, 
               branch=None, 
               work_location=None, 
               shift_type="Day"):
    try:
        file_url = None
        if status != "OUT" and base64_image and filename:
            image_data = decode_base64(base64_image)
            if not image_data:
                return {"status": "error", "message": "Invalid base64 data"}

            folder_path = frappe.utils.get_files_path("attendance", is_private=False)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "wb") as f:
                f.write(image_data)

            file_url = f"/files/attendance/{filename}"

            file_doc = frappe.get_doc({
                "doctype": "File",
                "file_name": filename,
                "file_url": file_url,
                "is_private": 0,
            })
            file_doc.insert(ignore_permissions=True)
            frappe.db.commit()

        if status == "IN":
            response = check_in_employee_for_shift(employee, branch, work_location, shift_type)
        elif status == "OUT":
            response = check_out_employee_for_shift(employee)

        checkin = frappe.get_doc({
            "doctype": "Employee Checkin",
            "employee": employee,
            "log_type": status,
            "employee_image": file_url,
            "branch": branch,
            "shift_type": shift_type,
            "work_location": work_location,
        })
        checkin.flags.ignore_hooks = True
        checkin.insert(ignore_permissions=True)
        frappe.db.commit()

        if status == "IN":
            attendance = frappe.get_doc({
                "doctype": "Attendance",
                "employee": employee,
                "attendance_date": today(),
                "status": "Present",
                "branch": branch,
                "employee_image": file_url,
                "shift_type": shift_type,
                "in_time": now(),
            })
            attendance.insert(ignore_permissions=True)
            attendance.submit()
            frappe.db.commit()

        return {
            "status": response.get("status"),
            "message": response.get("message"),
            "image_url": file_url,
        }

    except Exception as e:
        frappe.log_error(title="Employee Checkin Error", message=frappe.get_traceback())
        return {"status": "error", "message": str(e)}



@frappe.whitelist()
def attendance(employee, 
               status, 
               base64_image=None, 
               filename=None, 
               branch=None, 
               work_location=None, 
               shift_type="Day"):
    try:
        file_url = None

        if base64_image and filename:
            image_data = decode_base64(base64_image)
            if not image_data:
                return {"status": "error", "message": "Invalid base64 data"}

            folder_path = frappe.utils.get_files_path("attendance", is_private=False)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            file_path = os.path.join(folder_path, filename)
            with open(file_path, "wb") as f:
                f.write(image_data)

            file_url = f"/files/attendance/{filename}"

            file_doc = frappe.get_doc({
                "doctype": "File",
                "file_name": filename,
                "file_url": file_url,
                "is_private": 0,
            })
            file_doc.insert(ignore_permissions=True)
            frappe.db.commit()

        attendance_doc = frappe.get_doc({
            "doctype": "Attendance",
            "employee": employee,
            "attendance_date": today(),
            "status": status,
            "branch": branch,
            "employee_image": file_url,
            "shift_type": shift_type,
            "in_time": now() if status in ["Present", "Half Day", "Work From Home"] else None
        })
        attendance_doc.insert(ignore_permissions=True)
        attendance_doc.submit()
        frappe.db.commit()

        if status in ["Present", "Half Day", "Work From Home"]:
            response = check_in_employee_for_shift(employee, branch, work_location, shift_type)

            checkin = frappe.get_doc({
                "doctype": "Employee Checkin",
                "employee": employee,
                "log_type": "IN",
                "employee_image": file_url,
                "branch": branch,
                "shift_type": shift_type,
                "work_location": work_location,
            })
            checkin.flags.ignore_hooks = True
            checkin.insert(ignore_permissions=True)
            frappe.db.commit()
        else:
            response = {"status": "success", "message": f"Attendance marked as {status}"}

        return {
            "status": response.get("status"),
            "message": response.get("message"),
            "image_url": file_url,
        }

    except Exception as e:
        frappe.log_error(title="Employee Attendance Error", message=frappe.get_traceback())
        return {"status": "error", "message": str(e)}


def check_in_employee_for_shift(employee, branch, work_location, shift_type):
    
    if not branch or not work_location:
        return {"status": "error", "message": "Employee must have a Branch and Work Location!"}

    shift_count = frappe.db.count("Shift Log", {
        "employee": employee,
        "check_in_time": [">=", today()]
    })

    if shift_count >= 2:
        return {"status": "error", "message": "This employee has already completed 2 shifts today!"}

    shift_log = frappe.get_doc({
        "doctype": "Shift Log",
        "employee": employee,
        "branch": branch,
        "work_location": work_location,
        "shift_type": shift_type,
        "check_in_time": now()
    })
    shift_log.insert(ignore_permissions=True)
    frappe.db.commit()

    return {"status": "success", "message": "Check-in successful!", "shift_id": shift_log.name}


def check_out_employee_for_shift(employee):

    shift = frappe.db.get_value("Shift Log", {
        "employee": employee,
        "check_out_time": ["is", "null"]
    }, "name")

    if not shift:
        return {"status": "error", "message": "No active shift found for this employee!"}

    shift_doc = frappe.get_doc("Shift Log", shift)
    shift_doc.check_out_time = now()
    shift_doc.save()
    frappe.db.commit()

    return {"status": "success", "message": "Check-out successful!"}


@frappe.whitelist()
def get_employees_for_bulk_attendance(branch=None):
    user = frappe.session.user
    employee_id = frappe.db.get_value("Employee", {"user_id": user}, "name")

    branches = frappe.get_all(
        "Branch",
        filters={"branch_manager": employee_id},
        pluck="name"
    )

    if not branches:
        return {"error": "No branches assigned"}

    filters = {"branch": ["in", branches]}
    if branch:
        filters["branch"] = branch

    employees = frappe.get_all(
        "Employee",
        filters=filters,
        fields=["name", "employee_name", "designation","shift", "branch"],
        order_by="employee_name asc",
    )

    return employees

@frappe.whitelist()
def get_branches_for_manager():
    user = frappe.session.user
    employee_id = frappe.db.get_value("Employee", {"user_id": user}, "name")

    if not employee_id:
        return []

    branches = frappe.get_all(
        "Branch",
        filters={"branch_manager": employee_id},
        pluck="name"
    )

    return branches
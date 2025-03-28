import frappe
from custom_kcs.src.utils.base64_utils import decode_base64
import os
from frappe.utils import now, get_time, today

@frappe.whitelist()
def attendance(employee, log_type, base64_image=None, filename=None, branch=None, work_location=None, shift_type="Day"):
    try:
        file_url = None
        if log_type != "OUT" and base64_image and filename:
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

        if log_type == "IN":
            response = check_in_employee_for_shift(employee, branch, work_location, shift_type)
        elif log_type == "OUT":
            response = check_out_employee_for_shift(employee)

        checkin = frappe.get_doc({
            "doctype": "Employee Checkin",
            "employee": employee,
            "log_type": log_type,
            "employee_image": file_url,
            "branch": branch,
            "shift_type": shift_type,
            "work_location": work_location,
        })
        checkin.flags.ignore_hooks = True
        checkin.insert(ignore_permissions=True)
        frappe.db.commit()

        if log_type == "IN":
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

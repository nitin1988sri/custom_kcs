import frappe, math
from custom_kcs.src.utils.base64_utils import decode_base64
import os
from frappe.utils import now, get_time, today
from frappe.utils import now, today, now_datetime
from frappe.utils.file_manager import save_file
from custom_kcs.src.http_response import (
    _respond,
    _ok, _created, _bad_request, _forbidden,
    _not_found, _conflict, _unprocessable, _server_error,
)


@frappe.whitelist()
def bulk_attendance(data):
    data = frappe.parse_json(data)
    responses = []
    for entry in data:
        res = attendance(
            employee = entry.get("employee"),
            status = entry.get("status"),
            attendance_date= entry.get("attendance_date"),
            shift_type = entry.get("shift_type"),
            branch = entry.get("branch")
        )
        responses.append(res)

    return responses


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    p1 = math.radians(lat1); p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1); dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def _attach_image_to_attendance(att, base64_image, filename=None, image_fieldname="image"):
    """Attendance पर image attach करे और 'image' फील्ड में URL सेट करे."""
    if not base64_image:
        return None

    old_files = frappe.get_all(
        "File",
        filters={
            "attached_to_doctype": "Attendance",
            "attached_to_name": att.name,
            "attached_to_field": image_fieldname,
        },
        pluck="name",
    )
    for fid in old_files:
        frappe.delete_doc("File", fid, ignore_permissions=True)

    if not filename:
        filename = f"attendance_{att.employee}_{now_datetime().strftime('%Y%m%d%H%M%S')}.png"

    content = decode_base64(base64_image)
    if not content:
        frappe.throw("Invalid base64 data")

    fdoc = save_file(
        fname=filename,
        content=content,
        dt="Attendance",
        dn=att.name,
        is_private=0,
    )

    fdoc.attached_to_field = image_fieldname
    fdoc.save(ignore_permissions=True)

    setattr(att, image_fieldname, fdoc.file_url)
    att.save(ignore_permissions=True)

    return fdoc.file_url

@frappe.whitelist(methods=["POST"])
def attendance(employee, status, attendance_date=None, shift_type=None,
               branch=None, base64_image=None, filename=None,
               latitude=None, longitude=None):

    # --- Require essentials ---
    if not employee or not shift_type:
        return _bad_request("employee, shift_type and branch are required.")

    day = attendance_date or today()

    # --- Geo validations ---
    if not (latitude and longitude):
        return _bad_request("Latitude and Longitude are required.")

    branch_row = frappe.db.get_value(
        "Branch", branch, ["latitude", "longitude", "geofence_radius_m"], as_dict=True
    )
    if not branch_row or not branch_row.latitude or not branch_row.longitude:
        return _unprocessable("Branch coordinates not set")

    radius_m = float(branch_row.geofence_radius_m or 50)
    dist = haversine(float(latitude), float(longitude),
                     float(branch_row.latitude), float(branch_row.longitude))
    if dist > radius_m:
        return _forbidden(f"You are {int(dist)} m away. Allowed {int(radius_m)} m.")

    existing = frappe.db.get_value(
        "Attendance",
        {
            "employee": employee,
            "attendance_date": day,
            "shift": shift_type,
            "docstatus": ["<", 2],  
        },
        "name",
    )
    if existing:
        return _conflict(f"Attendance already exists for {employee} on {day} in shift '{shift_type}'.", attendance_id=existing)


    total_today = frappe.db.count(
        "Attendance",
        {"employee": employee, "attendance_date": day, "docstatus": ["<", 2]},
    )
    if total_today >= 2:
        return _conflict(f"Max 2 attendances allowed per day. Already have {total_today} on {day}.")


    att = frappe.get_doc({
        "doctype": "Attendance",
        "employee": employee,
        "attendance_date": day,
        "status": status,
        "branch": branch,
        "shift": shift_type,
        "in_time": now() if status in ["Present"] else None,
        "latitude": latitude,
        "longitude": longitude,
    })
    att.insert(ignore_permissions=True)

    result = mark_checking(employee, status, branch, shift_type)

    if result.get("status") == "success":
        att.submit()
        frappe.db.commit()
        return {
            "status": "success",
        }

    att.delete()
    frappe.db.commit()
    return _conflict(result.get("message") or "Failed to mark checking")


def mark_checking(employee, status, branch, shift_type):
    try:
        if status in ["Present", "Absent"]: 
            response = check_in_employee_for_shift(employee, branch, shift_type)
            checkin = frappe.get_doc({
                "doctype": "Employee Checkin",
                "employee": employee,
                "log_type": "IN",
                "branch": branch,
                "shift_type": shift_type
            })
            checkin.flags.ignore_hooks = True
            checkin.insert(ignore_permissions=True)
            frappe.db.commit()
        else:
            response = {"status": "success", "message": f"Attendance marked as {status}"}

        return {
            "status": response.get("status"),
            "message": response.get("message"),
        }
    except Exception as e:
        frappe.log_error(title="Employee Attendance Error", message=frappe.get_traceback())
        return {"status": "error", "message": str(e)}


def check_in_employee_for_shift(employee, branch, shift_type):
    
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
def get_employees_for_bulk_attendance_bkp(branch=None):
    user = frappe.session.user
    employee_id = frappe.db.get_value("Employee", {"user_id": user}, "name")

    branches = frappe.get_all(
        "Branch",
        filters={"branch_manager": employee_id},
        pluck="name"
    )

    if not branches:
        return {"error": "No branches assigned"}

    if branch:
        branches = [branch]

    placeholders = ','.join(['%s'] * len(branches))

    today = frappe.utils.today()

    query = f"""
        SELECT e.name, e.employee_name, e.designation, e.shift, e.branch
        FROM `tabEmployee` e
        WHERE e.branch IN ({placeholders})
        AND NOT EXISTS (
            SELECT 1 FROM `tabAttendance` a
            WHERE a.employee = e.name
            AND a.attendance_date = %s
        )
        ORDER BY e.employee_name ASC
    """

    params = branches + [today]

    employees = frappe.db.sql(query, params, as_dict=True)

    return employees

@frappe.whitelist()
def get_employees_for_bulk_attendance(branch=None, shift_type=None):
    user = frappe.session.user
    employee_id = frappe.db.get_value("Employee", {"user_id": user}, "name")

    branches = frappe.get_all(
        "Branch",
        filters={"branch_manager": employee_id},
        pluck="name"
    )

    if not branches:
        return {"error": "No branches assigned"}

    if branch:
        branches = [branch]

    placeholders = ','.join(['%s'] * len(branches))
    today = frappe.utils.today()

    # Prepare base query and conditions
    query = f"""
        SELECT e.name, e.employee_name, e.designation, e.shift, e.branch
        FROM `tabEmployee` e
        WHERE e.branch IN ({placeholders})
    """

    params = branches

    if shift_type:
        query += " AND e.shift = %s"
        params.append(shift_type)

    query += """
        AND NOT EXISTS (
            SELECT 1 FROM `tabAttendance` a
            WHERE a.employee = e.name
            AND a.attendance_date = %s
        )
        ORDER BY e.employee_name ASC
    """

    params.append(today)

    employees = frappe.db.sql(query, params, as_dict=True)

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
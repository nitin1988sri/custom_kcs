import frappe
from frappe import _
from datetime import date
from math import radians, sin, cos, asin, sqrt

def _today_str():
    return date.today().isoformat()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000.0
    dlat = radians(lat2 - lat1); dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    c = 2*asin(sqrt(a))
    return R*c

def _get_branch_coords(branch):
    row = frappe.db.get_value("Branch", branch, ["latitude","longitude"], as_dict=True)
    if not row or row.latitude is None or row.longitude is None:
        frappe.throw(_("Branch coordinates not set for {0}").format(branch))
    return float(row.latitude), float(row.longitude)

def _validate_geofence(branch, lat, lon, max_meters=50):
    blat, blon = _get_branch_coords(branch)
    dist = haversine(float(lat), float(lon), blat, blon)
    if dist > max_meters:
        frappe.throw(_("You are {0} meters away from branch. Stay within {1} m.")
                     .format(int(dist), max_meters))

def _get_active_in_log(employee):
    rows = frappe.get_all("Employee Checkin",
        filters={"employee": employee, "log_type": "IN", "shift_actual_end": ["is","not set"]},
        fields=["name","time","branch","shift","selected_shift"],
        order_by="time desc", limit=1
    )
    return rows[0] if rows else None

def _today_in_count(employee):
    return frappe.db.count("Employee Checkin", {
        "employee": employee, "log_type": "IN",
        "time": [">=", _today_str() + " 00:00:00"]
    })

def _split_assignments(employee, emp_primary_shift):

    rows = frappe.get_all("Overtime",
        filters={
            "employee": employee,
            "status": "Active",
            "start_date": ["<=", _today_str()],
            "end_date": [">=", _today_str()]
        },
        fields=["name","original_branch","overtime_branch","start_date","end_date","shift_type"],
        order_by="start_date asc"
    )
    branch_switch, overtime = [], []
    for r in rows:
        obj = {
            "name": r.overtime_branch,
            "assignment_id": r.name,
            "date_from": r.start_date,
            "date_to": r.end_date,
            "shift": r.shift
        }
        if (r.shift == emp_primary_shift):
            branch_switch.append(obj)         
        else:
            overtime.append(obj)             
    return branch_switch, overtime

@frappe.whitelist(methods=["GET"])
def get_employee_context(employee_id=None):
    if not employee_id:
        employee_id = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
    if not employee_id:
        return {"status":"error","message":"Employee not linked."}

    emp = frappe.db.get_value("Employee", employee_id, ["branch","shift"], as_dict=True)
    primary_branch_obj = None
    if emp and emp.branch:
        primary_branch_obj = {
            "name": emp.branch,
            "shift": emp.shift,   
            "type": "PRIMARY"
        }

    branch_switch, overtime = _split_assignments(employee_id, emp.shift if emp else None)
    #active = _get_active_in_log(employee_id)

    data = {
        "primary_branch": primary_branch_obj,
        "branch_switch_branches": branch_switch,
        "overtime_branches": overtime,

        # "is_checked_in": bool(active),
        # "current_checkin": active or None,
        # "today_shifts_count": _today_in_count(employee_id)
    }
    return {"status":"success","data":data}

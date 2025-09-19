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
        fields=["name","time","branch","shift_kind","selected_shift"],  # adjust to your fieldnames
        order_by="time desc", limit=1
    )
    return rows[0] if rows else None

def _today_in_count(employee):
    return frappe.db.count("Employee Checkin", {
        "employee": employee, "log_type": "IN",
        "time": [">=", _today_str() + " 00:00:00"]
    })

def _att_for(employee: str, day: str, shift_type: str | None, branch: str | None):
    """Return attendance name if exists (docstatus < 2), else None."""
    filters = {
        "employee": employee,
        "attendance_date": day,
        "docstatus": ["<", 2],
    }
    if shift_type:
        filters["shift"] = shift_type
    if branch:
        filters["branch"] = branch
    return frappe.db.get_value("Attendance", filters, "name")

def _split_assignments(employee: str, emp_primary_shift: str | None):
    """
    Overtime rows active today -> split:
      - branch_switch: same shift as employee.shift (Regular @ other branch)
      - overtime:      different shift (OT)
    NOTE: Overtime doctype must have field 'shift_type'
    """
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
        item = {
            "name": r.overtime_branch,       # branch name
            "shift": r.shift_type            # <-- FIXED: earlier you used r.shift (None)
        }
        if emp_primary_shift and r.shift_type == emp_primary_shift:
            branch_switch.append(item)       # same shift -> branch switch (regular)
        else:
            overtime.append(item)            # different shift -> overtime
    return branch_switch, overtime

@frappe.whitelist(methods=["GET"])
def get_employee_context(employee_id=None):
    # resolve employee
    if not employee_id:
        employee_id = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
    if not employee_id:
        return {"status":"error","message":"Employee not linked."}

    # normalize date
    day = date.today().isoformat()

    emp = frappe.db.get_value("Employee", employee_id, ["branch","shift"], as_dict=True)
    primary_branch_obj = None
    if emp and emp.branch:
        primary_branch_obj = {
            "name": emp.branch,
            "shift": emp.shift
        }

    # split assignments for *today* by shift matching
    branch_switch, overtime = _split_assignments(employee_id, emp.shift if emp else None)

    # Effective "primary for the day" = branch_switch (if exists) else true primary
    effective_primary = None
    if branch_switch:
        # pick first branch switch as today's effective primary
        effective_primary = {
            "name": branch_switch[0]["name"],
            "shift": emp.shift
        }
    elif primary_branch_obj:
        effective_primary = {
            **primary_branch_obj
        }

    # ---- Attendance flags ----
    # primary/effective
    if effective_primary:
        att_id = _att_for(employee_id, day, shift_type=effective_primary["shift"], branch=effective_primary["name"])
        effective_primary["is_marked"] = bool(att_id)

    # each overtime branch
    ot_list = []
    for ot in overtime:
        att_id = _att_for(employee_id, day, shift_type=ot["shift"], branch=ot["name"])
        ot_list.append({
            **ot,
            "is_marked": bool(att_id)
        })

    # build payload
    payload = {
        "employee": employee_id,
        "primary_branch": effective_primary,   # may be None if no Employee.branch
        "overtime_branches": ot_list
    }
    return {"status": "success", "data": payload}

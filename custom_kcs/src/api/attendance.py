import frappe
from frappe.utils import get_first_day, get_last_day, today, getdate
from datetime import date


@frappe.whitelist(methods=["GET"])
def get_my_attendance(
    month: str | None = None,
    year: str | None = None,
):

    # --- Resolve session user & employee ---
    session_user = (frappe.session.user or "Guest").lower()
    if session_user == "guest":
        frappe.throw("Please login to view your attendance.", frappe.PermissionError)

    emp = frappe.db.get_value(
        "Employee", {"user_id": session_user, "status": "Active"}, "name"
    )
    if not emp:
        frappe.throw(f"Active Employee not found for user '{session_user}'.", frappe.DoesNotExistError)

    # --- Compute date range using only month/year ---
    today_dt = getdate(today())

    # Validate/normalize inputs
    if month and month != "all" and not str(month).isdigit():
        frappe.throw("Parameter 'month' must be 1-12 or 'all'")
    if year and not str(year).isdigit():
        frappe.throw("Parameter 'year' must be a 4-digit year like 2025")

    if year and month == "all":
        y = int(year)
        fdt = date(y, 1, 1)
        tdt = date(y, 12, 31)
    elif month and str(month).isdigit():
        y = int(year) if year else today_dt.year
        m = int(month)
        fdt = get_first_day(date(y, m, 1))
        tdt = get_last_day(date(y, m, 1))
    elif year and not month:
        y = int(year)
        fdt = date(y, 1, 1)
        tdt = date(y, 12, 31)
    else:
        # Default: current month
        fdt = get_first_day(today_dt)
        tdt = get_last_day(today_dt)

    fields = [
        "branch",
        "shift",
        "attendance_date",
        "status",
    ]
    meta = frappe.get_meta("Attendance")
    optional_fields = [
        "late_entry",
        "early_exit",
        "shift",
        "custom_latitude",
        "custom_longitude",
        "custom_address",
    ]
    for f in optional_fields:
        if meta.has_field(f):
            fields.append(f)

    rows = frappe.get_all(
        "Attendance",
        filters={
            "employee": emp,
            "attendance_date": ["between", [str(fdt), str(tdt)]],
        },
        fields=fields,
        order_by="attendance_date asc",
    )

    return {
        "success": True,
        "data": rows,
    }

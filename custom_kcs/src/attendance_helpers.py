import frappe
from frappe import _

# --- detect "Shift" fieldname on Overtime (shift/shift_type/...) ---
def _find_shift_field(doctype="Overtime"):
    meta = frappe.get_meta(doctype)
    candidates = ["shift_type"]
    for fn in candidates:
        if meta.has_field(fn):
            return fn
    for df in meta.fields:
        if (df.label or "").strip().lower() in ("shift", "shift type"):
            return df.fieldname
    return None

@frappe.whitelist(allow_guest=False)  # token या logged-in यूज़र से कॉल करें
def resolve_effective_branch_shift(employee_id: str, attendance_date: str | None = None):
   
    if not employee_id:
        frappe.throw(_("Employee is required"))

    day = attendance_date or frappe.utils.today()

    emp = frappe.db.get_value("Employee", employee_id, ["branch", "shift"], as_dict=True)
    if not emp:
        frappe.throw(_("Employee not found"))

    # Fetch active OT rows for that date
    shift_field = _find_shift_field("Overtime")
    fields = ["name", "overtime_branch", "start_date", "end_date"]
    if shift_field:
        fields.append(shift_field)

    rows = frappe.get_all(
        "Overtime",
        filters={
            "employee": employee_id,
            "status": "Active",
            "start_date": ["<=", day],
            "end_date": [">=", day],
        },
        fields=fields,
        order_by="start_date asc",
    )

    branch_switch = []
    overtime = []

    for r in rows:
        ot_branch = r.get("overtime_branch")
        ot_shift = r.get(shift_field) if shift_field else None
        obj = {
            "branch": ot_branch,
            "shift": ot_shift,
            "assignment_id": r.get("name"),
        }
        if shift_field and emp.shift:
            # same shift => branch switch (regular), else overtime
            if ot_shift == emp.shift:
                branch_switch.append(obj)
            else:
                overtime.append(obj)
        else:
            # अगर Overtime में shift field ही नहीं है:
            if ot_branch == emp.branch:
                overtime.append(obj)           # same branch => extra shift => OT
            else:
                branch_switch.append(obj)      # other branch => branch switch

    # Priority selection
    if branch_switch:
        pick = branch_switch[0]
        return {"branch": pick["branch"], "shift": emp.shift, "mode": "BRANCH_SWITCH", "assignment_id": pick["assignment_id"]}

    if overtime:
        pick = overtime[0]
        return {"branch": pick["branch"], "shift": pick["shift"] or emp.shift, "mode": "OVERTIME", "assignment_id": pick["assignment_id"]}

    # Fallback: primary
    return {"branch": emp.branch, "shift": emp.shift, "mode": "PRIMARY", "assignment_id": None}

import frappe
from frappe import _


@frappe.whitelist(allow_guest=False) 
def resolve_effective_branch_shift(employee_id: str, attendance_date: str | None = None):
 
    if not employee_id:
        frappe.throw(_("Employee is required"))

    day = attendance_date or frappe.utils.today()

    emp = frappe.db.get_value("Employee", employee_id, ["branch", "shift"], as_dict=True)
    if not emp:
        frappe.throw(_("Employee not found"))

    fields = ["name", "overtime_branch", "start_date", "end_date", "shift_type"]
   

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

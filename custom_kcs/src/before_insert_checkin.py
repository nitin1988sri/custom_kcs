import frappe
from frappe.utils import now, get_time, today

def before_insert_checkin(doc, event):

    if getattr(doc, "flags", None) and doc.flags.get("ignore_hooks"):
        return

    employee_doc = frappe.get_doc("Employee", doc.employee)

    doc.branch = employee_doc.branch or frappe.throw("Employee must have a Branch assigned!")
    if not doc.work_location:
            frappe.throw("Work Location must be provided in the form!")

    current_time = get_time(now().split(" ")[1])  

    shift_type = frappe.db.sql(
        """
        SELECT name FROM `tabShift Type`
        WHERE start_time <= %s AND end_time >= %s
        LIMIT 1
        """,
        (current_time, current_time),
        as_dict=True
    )

    if not shift_type:
        frappe.throw("No Shift Type found for the current time!")

    shift_type_name = shift_type[0]["name"]

    shift_count = frappe.db.count(
        "Shift Log",
        filters={"employee": doc.employee, "check_in_time": [">=", today()]}
    )

    if shift_count >= 2:
        frappe.throw("Employee cannot check-in more than 2 times in a single day!")

    shift_log = frappe.get_doc({
        "doctype": "Shift Log",
        "employee": doc.employee,
        "branch": doc.branch,
        "work_location": doc.work_location,
        "shift_type": shift_type_name,
        "check_in_time": now()
    })
    shift_log.insert(ignore_permissions=True)
    frappe.db.commit()

    doc.shift_log = shift_log.name

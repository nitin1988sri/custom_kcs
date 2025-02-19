import frappe
from frappe.utils import now, get_time, today

def before_insert_checkin(doc, event):

    if getattr(doc, "flags", None) and doc.flags.get("ignore_hooks"):
        return

   # Ensure required fields are provided via the form (do not pull from Employee doctype)
    if not doc.branch:
        frappe.throw("Branch must be provided in the form!")
    if not doc.work_location:
        frappe.throw("Work Location must be provided in the form!")
    
    if doc.log_type == "IN":
        # ----- For Check-In -----
        # Extract current time (as a string) to match Shift Type records
        current_time = get_time(now().split(" ")[1])
        current_time_str = str(current_time)  # e.g. "19:08:25"

        # Fetch the Shift Type record that matches the current time.
        # This query also handles cases where the shift spans midnight.
        shift_type = frappe.db.sql(
            """
            SELECT name FROM `tabShift Type`
            WHERE 
                (%s BETWEEN start_time AND end_time)
                OR (start_time > end_time AND (%s >= start_time OR %s <= end_time))
            LIMIT 1
            """,
            (current_time_str, current_time_str, current_time_str),
            as_dict=True
        )

        if not shift_type:
            frappe.throw("No Shift Type found for the current time!")
        shift_type_name = shift_type[0]["name"]

        # Ensure the employee has not checked in more than 2 times today.
        shift_count = frappe.db.count("Shift Log", {
            "employee": doc.employee,
            "check_in_time": [">=", today()]
        })
        if shift_count >= 2:
            frappe.throw("Employee cannot check-in more than 2 times in a single day!")

        # Create a new Shift Log entry.
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

        # Link the created Shift Log to the Employee Checkin record.
        doc.shift_log = shift_log.name

    elif doc.log_type == "OUT":
        # ----- For Check-Out -----
        # Find an active Shift Log for this employee (i.e. one with no check-out time)
        active_shift = frappe.db.get_value("Shift Log", {
            "employee": doc.employee,
            "check_out_time": ["is", "null"]
        }, "name")

        if not active_shift:
            frappe.throw("No active shift found for this employee!")
        
        shift_doc = frappe.get_doc("Shift Log", active_shift)
        shift_doc.check_out_time = now()
        shift_doc.save(ignore_permissions=True)
        frappe.db.commit()

        # Link this Shift Log to the Employee Checkin record.
        doc.shift_log = active_shift

    else:
        frappe.throw("Invalid log type!")

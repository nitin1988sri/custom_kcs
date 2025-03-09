import frappe

def validate_duplicate_attendance(doc, method):
    existing_attendance = frappe.get_all(
        "Attendance",
        filters={
            "employee": doc.employee,
            "attendance_date": doc.attendance_date,
            "shift": doc.shift,  
            "docstatus": ["!=", 2] 
        },
        fields=["name"]
    )

    if existing_attendance:
        frappe.throw(
            f"Duplicate Attendance: Attendance for employee {doc.employee} is already marked for the date {doc.attendance_date} and shift {doc.shift}."
        )

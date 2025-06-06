import frappe
from frappe import _

@frappe.whitelist(allow_guest= True)
def get_allocated_equipment(employee):
    def get_equipment_list(employee):
    equipment_list = frappe.get_all("Equipment Master", fields=["name", "equipment_name", "description"])

    # Step 1: Filter allocations for this employee where status = "Allocated"
    allocated_items = frappe.get_all(
        "Equipment Allocation",
        filters={
            "employee": employee,
            "status": "Allocated"
        },
        fields=["equipment", "allocation_date"]
    )
    allocated_map = {item["equipment"]: item for item in allocated_items}

    # Step 2: Prepare merged response
    final_list = []
    for eq in equipment_list:
        allocated_info = allocated_map.get(eq["name"])
        final_list.append({
            "equipment": eq["equipment_name"],
            "description": eq.get("description"),
            "is_allocated": bool(allocated_info),
            "allocation_date": allocated_info["allocation_date"] if allocated_info else None
        })

    return final_list

@frappe.whitelist(allow_guest=True)
def request_equipment(employee, equipment):
    if frappe.db.exists("Equipment Allocation", {"employee": employee, "equipment": equipment}):
        return {"message": _("Already requested or assigned.")}

    doc = frappe.get_doc({
        "doctype": "Equipment Allocation",
        "employee": employee,
        "equipment": equipment,
        "allocation_date": frappe.utils.nowdate(),
        "condition": "New",
        "remarks": "Requested from mobile app"
    })
    doc.insert()
    return {"message": _("Equipment request submitted.")}

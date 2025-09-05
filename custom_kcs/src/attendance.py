import frappe
import math
from frappe.model.document import Document
from frappe.utils import nowdate

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

@frappe.whitelist()
def mark_attendance_with_gps(employee, shift, latitude, longitude, base64_image=None):
    branch = frappe.db.get_value("Employee", employee, "branch")
    branch_coords = frappe.db.get_value("Branch", branch, ["latitude", "longitude"], as_dict=True)

    if not branch_coords or not branch_coords.latitude or not branch_coords.longitude:
        frappe.throw("Branch latitude/longitude not found")

    distance = haversine(float(latitude), float(longitude), float(branch_coords.latitude), float(branch_coords.longitude))

    if distance > 50:
        frappe.throw(f"You are {int(distance)} meters away from branch. Please move within 50 meters.")

    doc = frappe.get_doc({
        "doctype": "Attendance",
        "employee": employee,
        "status": "Present",
        "attendance_date": nowdate(),
        "shift": shift,
        "branch": branch,
        "latitude": latitude,
        "longitude": longitude,
        "branch_lat": branch_coords.latitude,
        "branch_lng": branch_coords.longitude,
        "distance_m": round(distance, 2)
    })

    # Optional: Save photo
    if base64_image:
        from frappe.utils.file_manager import save_file
        import base64
        img_data = base64.b64decode(base64_image)
        file_name = f"{employee}_{frappe.utils.now_datetime()}.jpg"
        saved = save_file(file_name, img_data, "Attendance", None, is_private=0)
        doc.image = saved.file_url

    doc.insert()
    return {"message": "Attendance marked", "docname": doc.name}

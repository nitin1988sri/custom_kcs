import frappe
from custom_kcs.src.utils.base64_utils import decode_base64
import os


@frappe.whitelist()
def attendance(employee, log_type, base64_image=None, filename=None):
    try:
        file_url = None

        if log_type != "OUT" and base64_image and filename:
            image_data = decode_base64(base64_image)
            if not image_data:
                return {"status": "error", "message": "Invalid base64 data"}

            folder_path = frappe.utils.get_files_path("attendance", is_private=False)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "wb") as f:
                f.write(image_data)

            file_url = f"/files/attendance/{filename}"

            file_doc = frappe.get_doc(
                {
                    "doctype": "File",
                    "file_name": filename,
                    "file_url": file_url,
                    "is_private": 0,
                }
            )
            file_doc.insert(ignore_permissions=True)
            frappe.db.commit()

        checkin = frappe.get_doc(
            {
                "doctype": "Employee Checkin",
                "employee": employee,
                "log_type": log_type,
                "employee_image": file_url,
            }
        )
        checkin.insert(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "message": "Check-in recorded successfully!",
            "image_url": file_url,
        }

    except Exception as e:
        frappe.log_error("Employee Checkin Error", str(e))
        return {"status": "error", "message": str(e)}

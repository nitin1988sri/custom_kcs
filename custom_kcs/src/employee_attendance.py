import frappe
from custom_kcs.src.utils.base64_utils import decode_base64

@frappe.whitelist()
def employee_checkin(employee, log_type, base64_image=None, filename=None):
    try:
        file_url = None  
        
        if log_type != "OUT" and base64_image and filename:
            image_data = decode_base64(base64_image)
            if not image_data:
                return {"status": "error", "message": "Invalid base64 data"}
            
            file_doc = frappe.get_doc({
                "doctype": "File",
                "file_name": filename,
                "content": image_data,
                "is_private": 1
            })
            file_doc.insert(ignore_permissions=True)
            frappe.db.commit()

            file_url = file_doc.file_url  

        checkin = frappe.get_doc({
            "doctype": "Employee Checkin",
            "employee": employee,
            "log_type": log_type,
            "employee_image": file_url  # Will be None if log_type is "OUT"
        })
        checkin.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"status": "success", "message": "Check-in recorded successfully!", "image_url": file_url}

    except Exception as e:
        frappe.log_error("Employee Checkin Error", str(e))
        return {"status": "error", "message": str(e)}

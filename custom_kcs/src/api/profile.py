import frappe
from frappe import _
from frappe.utils.file_manager import save_file

# --- Fixed fieldname on User only ---
USER_IMAGE_FIELD = "user_image"   # change to "image" if your User has that

def _my_employee() -> str | None:
    return frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")

def _set_user_image(user_name: str, base64_data: str, filename: str | None = None, private: bool = True) -> str:
    if not base64_data:
        frappe.throw(_("Image data is empty"))

    # delete old file(s) attached to this field
    old = frappe.get_all("File", {
        "attached_to_doctype": "User",
        "attached_to_name": user_name,
        "attached_to_field": USER_IMAGE_FIELD
    }, pluck="name")
    for fid in old:
        frappe.delete_doc("File", fid, ignore_permissions=True)

    # decode base64 (supports data:...;base64,xxx or raw base64)
    if "," in base64_data:
        base64_data = base64_data.split(",", 1)[1]
    try:
        content = frappe.utils.base64.b64decode(base64_data)
    except Exception:
        from custom_kcs.src.utils.base64_utils import decode_base64
        content = decode_base64(base64_data)
    if not content:
        frappe.throw(_("Invalid image base64 data"))

    if not filename:
        filename = f"profile_user_{user_name}.png"

    fdoc = save_file(filename, content, "User", user_name, is_private=private)
    frappe.db.set_value("User", user_name, USER_IMAGE_FIELD, fdoc.file_url, update_modified=False)
    return fdoc.file_url

# -------- GET PROFILE (User + Employee basics; image only on User) --------
@frappe.whitelist()
def get_profile(employee_id: str | None = None):
    user_id = frappe.session.user
    user_doc = frappe.get_doc("User", user_id)

    if not employee_id:
        employee_id = _my_employee()

    emp_block = None
    if employee_id:
        fields = ["name","employee_name","company","branch","department","designation",
                  "cell_number","personal_email","company_email","shift"]
        emp_block = frappe.db.get_value("Employee", employee_id, fields, as_dict=True)

    data = {
        "user": {
            "name": user_doc.name,
            "full_name": user_doc.full_name,
            "email": user_doc.email,
            "mobile_no": getattr(user_doc, "mobile_no", None),
            "image_url": getattr(user_doc, USER_IMAGE_FIELD, None)  # ONLY HERE
        },
        "employee": emp_block  # no image_url key here
    }
    return {"status": "success", "data": data}

@frappe.whitelist(methods=["POST"])
def update_profile(
    full_name: str | None = None,
    mobile_no: str | None = None,
    image_base64: str | None = None,
    private_image: int = 1
):
    user_id = frappe.session.user
    user_doc = frappe.get_doc("User", user_id)

    dirty = False
    if full_name and full_name.strip():
        user_doc.full_name = full_name.strip(); dirty = True
    if mobile_no and str(mobile_no).strip() and hasattr(user_doc, "mobile_no"):
        user_doc.mobile_no = str(mobile_no).strip(); dirty = True
    if dirty:
        user_doc.save(ignore_permissions=True)

    image_url = None
    if image_base64:
        image_url = _set_user_image(user_doc.name, image_base64, private=bool(int(private_image)))

    return {"status": "success", "message": "Profile updated", "data": {"user_image_url": image_url}}

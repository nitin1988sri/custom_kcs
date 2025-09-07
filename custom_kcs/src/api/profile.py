import frappe
from frappe import _
from frappe.utils.file_manager import save_file

# ---- FIXED FIELDNAMES (change if needed) ----
USER_IMAGE_FIELD = "user_image"      # अगर User में 'image' नाम का field है तो इसे "image" कर दें
EMPLOYEE_IMAGE_FIELD = "image"       # अगर Employee में 'full_length_photo' चाहिए तो यही बदल दें

def _employee_of_current_user() -> str | None:
    return frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")

def _set_image(doctype: str, name: str, fieldname: str, base64_data: str,
               filename: str | None = None, private: bool = True) -> str:
    """Old file हटाकर दिए गए field पर नई image set करता है (fixed fieldname)."""
    if not base64_data:
        frappe.throw(_("Image data is empty"))

    # old files for this specific field delete
    old = frappe.get_all("File",
        filters={"attached_to_doctype": doctype, "attached_to_name": name, "attached_to_field": fieldname},
        pluck="name",
    )
    for fid in old:
        frappe.delete_doc("File", fid, ignore_permissions=True)

    # decode: data:*;base64,.... या pure base64
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
        filename = f"profile_{doctype.lower()}_{name}.png"

    fdoc = save_file(filename, content, doctype, name, is_private=private)
    # field set (no autodetect)
    frappe.db.set_value(doctype, name, fieldname, fdoc.file_url, update_modified=False)
    return fdoc.file_url


# ---------- GET PROFILE ----------
@frappe.whitelist()
def get_profile(employee_id: str | None = None):
    """Current user का profile (User + linked Employee) fixed fields के साथ."""
    user_id = frappe.session.user
    user_doc = frappe.get_doc("User", user_id)

    if not employee_id:
        employee_id = _employee_of_current_user()

    data = {
        "user": {
            "name": user_doc.name,
            "full_name": user_doc.full_name,
            "email": user_doc.email,
            "mobile_no": getattr(user_doc, "mobile_no", None),
            "image_url": getattr(user_doc, USER_IMAGE_FIELD, None),  
        },
        "employee": None,
    }

    if employee_id:
        fields = ["name","employee_name","company","branch","department","designation","cell_number","personal_email","company_email","shift"]
        emp = frappe.db.get_value("Employee", employee_id, fields, as_dict=True)
        if emp:
            emp["image_url"] = frappe.db.get_value("Employee", employee_id, EMPLOYEE_IMAGE_FIELD)  # fixed field
            data["employee"] = emp

    return {"status": "success", "data": data}


# ---------- UPDATE PROFILE ----------
@frappe.whitelist(methods=["POST"])
def update_profile(
    full_name: str | None = None,
    mobile_no: str | None = None,
    image_base64: str | None = None,
    target: str = "both",          
    employee_id: str | None = None,
    private_image: int = 1
):
    """Fixed image fields use करता है; कोई auto-detect नहीं."""
    user_id = frappe.session.user
    user_doc = frappe.get_doc("User", user_id)

    dirty = False
    if full_name and full_name.strip():
        user_doc.full_name = full_name.strip(); dirty = True
    if mobile_no and str(mobile_no).strip():
        if hasattr(user_doc, "mobile_no"):
            user_doc.mobile_no = str(mobile_no).strip(); dirty = True
    if dirty:
        user_doc.save(ignore_permissions=True)

    if not employee_id:
        employee_id = _employee_of_current_user()
    else:
        my_emp = _employee_of_current_user()
        if my_emp and employee_id != my_emp:
            frappe.throw(_("You can only update your own employee profile."))

    image_urls = {}
    if image_base64:
        is_private = bool(int(private_image))

        if target in ("user", "both"):
            image_urls["user_image_url"] = _set_image("User", user_doc.name, USER_IMAGE_FIELD, image_base64, private=is_private)

        if employee_id and target in ("employee", "both"):
            image_urls["employee_image_url"] = _set_image("Employee", employee_id, EMPLOYEE_IMAGE_FIELD, image_base64, private=is_private)

    return {"status": "success", "message": "Profile updated", "data": image_urls}

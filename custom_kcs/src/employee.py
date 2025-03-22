import frappe
from datetime import date

@frappe.whitelist()
def get_branches_by_client(client):
    if not client:
        return []

    branches = frappe.get_all("Branch", filters={"client": client}, pluck="name")
    return branches

def validate_employee(doc, method):
    required_fields = ["company", "designation", "grade", "client", "branch", "shift", "department", "employment_type"]
    
    for field in required_fields:
        if not doc.get(field):
            frappe.throw(f"{frappe.get_meta('Employee').get_label(field)} is mandatory.")

@frappe.whitelist()
def get_active_contracts(doctype, txt, searchfield, start, page_len, filters):
    client = filters.get("client")
    branch = filters.get("branch")

    if not client or not branch:
        return []

    today = date.today()

    return frappe.db.sql("""
        SELECT name
        FROM `tabContract`
        WHERE
            party_name = %(client)s
            AND branch = %(branch)s
            AND start_date <= %(today)s
            AND end_date >= %(today)s
            AND name LIKE %(txt)s
        ORDER BY name ASC
        LIMIT %(start)s, %(page_len)s
    """, {
        "client": client,
        "branch": branch,
        "today": today,
        "txt": f"%{txt}%",
        "start": start,
        "page_len": page_len
    })
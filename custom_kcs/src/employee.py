import frappe

@frappe.whitelist()
def get_branches_by_client(client):
    if not client:
        return []

    branches = frappe.get_all("Branch", filters={"client": client}, pluck="name")
    return branches

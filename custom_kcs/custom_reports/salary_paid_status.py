import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"label": "Branch", "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 200},
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 100},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Salary Amount", "fieldname": "total_amount", "fieldtype": "Currency", "width": 150}
    ]

def get_data(filters):
    entries = frappe.get_all("Payroll Entry", filters={
        "docstatus": 1
    }, fields=["name", "posting_date", "status", "selected_customers", "selected_branches"])

    data = []
    for entry in entries:
        customers = frappe.parse_json(entry.selected_customers or "[]")
        branches = frappe.parse_json(entry.selected_branches or "[]")
        month = frappe.utils.formatdate(entry.posting_date, "MM-yyyy")

        total = frappe.db.sql("""
            SELECT SUM(rounded_total) FROM `tabSalary Slip` 
            WHERE payroll_entry = %s
        """, (entry.name,))[0][0] or 0

        for customer in customers:
            for branch in branches:
                data.append({
                    "client": customer,
                    "branch": branch,
                    "month": month,
                    "status": entry.status,
                    "total_amount": total
                })
    return data

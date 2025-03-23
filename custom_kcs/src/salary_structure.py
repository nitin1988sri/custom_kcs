import frappe
from frappe import _

def validate(doc, method):
    if not doc.company and not doc.customer:
        frappe.throw(_("Please select either Company or Customer in Salary Structure."))

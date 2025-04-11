
import frappe
from frappe import _

def create_customer_branch_map():
   if not frappe.db.table_exists("Customer Branch Map"):
        doc = frappe.new_doc("DocType")
        doc.name = "Customer Branch Map"
        doc.module = "Custom KCS"
        doc.custom = 1
        doc.istable = 1
        doc.show_name_in_global_search = 0
        doc.search_fields = "customer, branch"
        doc.fields = []

        doc.append("fields", {
            "fieldname": "customer",
            "fieldtype": "Link",
            "label": "Customer",
            "options": "Customer",
            "reqd": 1
        })

        doc.append("fields", {
            "fieldname": "branch",
            "fieldtype": "Link",
            "label": "Branch",
            "options": "Branch",
            "reqd": 1
        })

        doc.save(ignore_permissions=True)
        frappe.db.commit()

create_customer_branch_map()

def add_customer_branch_table_to_payroll_entry():
    if not frappe.db.exists("Custom Field", "Payroll Entry-customer_branch_filter"):
        doc = frappe.new_doc("Custom Field")
        doc.dt = "Payroll Entry"
        doc.fieldname = "customer_branch_filter"
        doc.label = "Customer Branch Filter"
        doc.fieldtype = "Table"
        doc.insert_after = "employees"
        doc.options = "Customer Branch Map"
        doc.depends_on = "eval:doc.docstatus==0"
        doc.hidden = 0
        doc.save()
        frappe.db.commit()

def remove_customer_branch_table_from_payroll_entry():
    if frappe.db.exists("Custom Field", "Payroll Entry-customer_branch_filter"):
        frappe.delete_doc("Custom Field", "Payroll Entry-customer_branch_filter")
        frappe.db.commit()
def create_html_field_in_payroll_entry():
    if not frappe.db.exists("Custom Field", "Payroll Entry-customer_branch_filter_html"):
        doc = frappe.new_doc("Custom Field")
        doc.dt = "Payroll Entry"
        doc.fieldname = "customer_branch_filter_html"
        doc.label = "Customer Branch Filter"
        doc.fieldtype = "HTML"
        doc.insert_after = "payroll_frequency"
        doc.depends_on = "eval:doc.docstatus==0"
        doc.hidden = 0
        doc.save()
        frappe.db.commit()


def run_all():
    remove_customer_branch_table_from_payroll_entry()
    create_html_field_in_payroll_entry()
run_all()          
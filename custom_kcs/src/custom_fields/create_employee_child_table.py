import frappe

def create_employee_child_table():
    if not frappe.db.exists("DocType", "Employee Detail"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Employee Detail",
            "module": "Custom kcs",
            "custom": 1,
            "istable": 1,
            "fields": [
                {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "Employee", "in_list_view": 1},
                {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "in_list_view": 1},
                {"fieldname": "designation", "label": "Designation", "fieldtype": "Link", "options": "Designation", "in_list_view": 1},
                {"fieldname": "shift", "label": "Shift", "fieldtype": "Data", "in_list_view": 1},
                {"fieldname": "branch", "label": "Branch", "fieldtype": "Link", "options": "Branch", "in_list_view": 1},
                {"fieldname": "date_of_joining", "label": "Date of joining", "fieldtype": "Date", "in_list_view": 1}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1}
            ]
        })
        doc.insert()
        frappe.db.commit()

# create_custom_fields({
#     "Contract": [
#         {
#             "fieldname": "employees_list",
#             "label": "Employees List",
#             "fieldtype": "Table",
#             "options": "Contract Employee Detail",
#             "insert_after": "roles",
#             "in_list_view": 0,
#             "read_only": 1,               
#             "cannot_add_rows": 1         
#         }
#     ]
# })

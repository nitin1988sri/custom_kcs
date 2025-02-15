import frappe
from frappe.model.document import Document
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def add_fields_to_branch():
    fields = [
        {
            'fieldname': 'city',
            'label': 'City',
            'fieldtype': 'Data',
            'insert_after': 'branch_name',
            'reqd': 0,
            'unique': 0,
        },
        {
            'fieldname': 'state',
            'label': 'State',
            'fieldtype': 'Data',
            'insert_after': 'city',
            'reqd': 0,
            'unique': 0,
        },
        {
            'fieldname': 'linked_client',
            'label': 'Linked Client',
            'fieldtype': 'Link',
            'options': 'Customer',
            'insert_after': 'state',
            'reqd': 0,
            'unique': 0,
        },
        {
            'fieldname': 'contact_name',
            'label': 'Contact Name',
            'fieldtype': 'Data',
            'insert_after': 'salary_structure',
            'reqd': 0,
            'unique': 0,
        },
        {
            'fieldname': 'contact_phone',
            'label': 'Phone',
            'fieldtype': 'Data',
            'insert_after': 'contact_name',
            'reqd': 0,
            'unique': 0,
        },
        {
            'fieldname': 'contact_email',
            'label': 'Email',
            'fieldtype': 'Data',
            'insert_after': 'contact_phone',
            'reqd': 0,
            'unique': 0,
        },
        {
            'fieldname': 'status',
            'label': 'Status',
            'fieldtype': 'Select',
            'options': 'Active\nInactive',
            'insert_after': 'contact_email',
            'reqd': 0,
            'unique': 0,
        }
    ]
    
    for field in fields:
        create_custom_field('Branch', field)

    frappe.db.commit()

add_fields_to_branch()

print("Fields have been successfully added to the Branch doctype.")

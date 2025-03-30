def add_incentive_days_field():
    from frappe.custom.doctype.custom_field.custom_field import create_custom_field

    field_def = {
        "dt": "Employee Incentive",
        "fieldname": "incentive_days",
        "label": "Incentive Days",
        "fieldtype": "Int",
        "insert_after": "incentive_amount"
    }

    create_custom_field("Employee Incentive", field_def)

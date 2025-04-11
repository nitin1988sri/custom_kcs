frappe.query_reports["Salary Paid Status"] = {
    "filters": [
        {
            "fieldname": "client",
            "label": __("Client"),
            "fieldtype": "Link",
            "options": "Customer",
        },
        {
            "fieldname": "month",
            "label": __("Month"),
            "fieldtype": "Date",
        }
    ]
};

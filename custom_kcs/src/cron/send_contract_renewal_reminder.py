import frappe

def send_contract_renewal_reminder():
    today = frappe.utils.today()
    contracts = frappe.get_all("Contract", 
        filters={"contract_end_date": ["<=", frappe.utils.add_days(today, 30)]},
        fields=["name", "customer", "contract_end_date"])
    
    for contract in contracts:
        frappe.sendmail(
            recipients=["admin@example.com"],
            subject=f"Contract Renewal Reminder: {contract['name']}",
            message=f"The contract {contract['name']} with {contract['customer']} is ending on {contract['contract_end_date']}. Please review for renewal."
        )

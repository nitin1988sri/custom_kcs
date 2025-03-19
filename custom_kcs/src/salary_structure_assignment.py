import frappe

@frappe.whitelist()
def get_salary_structure_details(salary_structure_name):
    """ Fetch the 'In Hand' Salary Component from Salary Structure """
    if not salary_structure_name:
        return {"error": "No Salary Structure provided"}

    salary_structure = frappe.get_doc("Salary Structure", salary_structure_name)
    
    in_hand_component = 0
    for component in salary_structure.earnings:
        if component.salary_component == "In Hand":  # Adjust as needed
            in_hand_component = component.amount
            break

    return {"in_hand": in_hand_component}

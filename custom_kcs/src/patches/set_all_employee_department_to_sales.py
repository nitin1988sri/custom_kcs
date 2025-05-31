import frappe

def run():
    try:
        if not frappe.db.exists("Department", "Sales"):
            frappe.get_doc({
                "doctype": "Department",
                "department_name": "Sales",
                "company": "KCS"  
            }).insert()
            frappe.db.commit()
            print("✅ 'Sales' department created.")

        # Update all employees
        frappe.db.set_value("Employee", {}, {
            "department": "Sales",
            "grade": "D"
        })        
        print("✅ All active employees updated to 'Sales' department.")

    except Exception as e:
        print(f"❌ Error during migration: {e}")

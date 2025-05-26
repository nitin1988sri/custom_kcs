import frappe
import csv

def create_state(state_name):
    state_name = state_name.strip()
    if not frappe.db.exists("State", {"state_name": state_name}):
        doc = frappe.get_doc({
            "doctype": "State",
            "state_name": state_name
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Inserted State: {state_name}")
        frappe.clear_cache()
    else:
        print(f"⚠️ State exists: {state_name}")

def create_city(city_name, state_name):
    city_name = city_name.strip()
    state_name = state_name.strip()

    # Ensure state exists before adding city
    if not frappe.db.exists("State", {"state_name": state_name}):
        print(f"❌ Cannot insert City {city_name}: Missing State {state_name}")
        return

    if not frappe.db.exists("City", {"city_name": city_name, "state": state_name}):
        doc = frappe.get_doc({
            "doctype": "City",
            "city_name": city_name,
            "state": state_name
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Inserted City: {city_name} ({state_name})")
    else:
        print(f"⚠️ City exists: {city_name} ({state_name})")

def run():
    # CSV path relative to site directory
    csv_path = frappe.get_site_path("public", "files", "Full_City_and_State_Migration_Data.csv")
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            state = row.get("State")
            city = row.get("City")
            if state and city:
                create_state(state)
                create_city(city, state)

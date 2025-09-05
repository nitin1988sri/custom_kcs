# apps/custom_kcs/custom_kcs/src/custom_fields/add_branch_geofence_section_fields.py

from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    custom_fields = {
        "Branch": [
            # Section for Geo Fencing
            {
                "fieldtype": "Section Break",
                "label": "Geo Fencing",
                "fieldname": "geo_fencing_sb",
                # "insert_after": "company",  # चाहें तो किसी existing field के बाद रखें; वरना अंत में जुड़ जाएगा
            },
            # Fields inside the section
            {
                "fieldtype": "Float",
                "label": "Latitude",
                "fieldname": "latitude",
                "precision": "6",
            },
            {
                "fieldtype": "Float",
                "label": "Longitude",
                "fieldname": "longitude",
                "precision": "6",
            },
            {
                "fieldtype": "Float",
                "label": "Geofence Radius (m)",
                "fieldname": "geofence_radius_m",
                "default": "50",
            },
        ]
    }
    create_custom_fields(custom_fields, ignore_validate=True)

def run_all():
    execute()

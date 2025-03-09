import frappe

def cancel_and_delete_all_attendance():
    try:
        # Fetch all attendance records
        attendance_records = frappe.get_all(
            "Attendance", fields=["name", "docstatus"]
        )

        if not attendance_records:
            print("No attendance records found.")
            return

        for record in attendance_records:
            doc = frappe.get_doc("Attendance", record["name"])

            # If the document is submitted (docstatus = 1), cancel it first
            if doc.docstatus == 1:
                doc.cancel()
                frappe.db.commit()
                frappe.logger().info(f"Cancelled Attendance {record['name']}")

            # Now delete the record
            frappe.delete_doc("Attendance", record["name"], force=True)
            frappe.logger().info(f"Deleted Attendance {record['name']}")

        frappe.db.commit()
        print("✅ All attendance records have been cancelled & deleted successfully.")

    except Exception as e:
        frappe.logger().error(f"❌ Failed to delete attendance: {str(e)}")
        print(f"❌ Error: {str(e)}")


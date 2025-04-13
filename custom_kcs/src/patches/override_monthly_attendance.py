def boot(bootinfo):
    print("🚀 Custom boot loaded")

    import hrms.hr.report.monthly_attendance_sheet.monthly_attendance_sheet as original_module

    original_get_emp = original_module.get_employee_related_details

    def patched_get_employee_related_details(filters):
        print("✅ Patched method hit")
        emp_map, group_by_param_values = original_get_emp(filters)

        if filters.get("branch"):
            filtered_emp_map = {
                emp: val for emp, val in emp_map.items()
                if val.get("branch") == filters.get("branch")
            }
            emp_map = filtered_emp_map

        return emp_map, group_by_param_values

    # Inject patch
    original_module.get_employee_related_details = patched_get_employee_related_details

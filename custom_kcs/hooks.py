
app_name = "custom_kcs"
app_title = "Custom Kcs"
app_publisher = "saurabh srivastava"
app_description = "Custome code for kcs"
app_email = "saurabh.srivastava.mca@gmail.com"
app_license = "mit"

# Apps
# ------------------
after_migrate = ["custom_kcs.src.custom_fields.add_fields_employee_checkIn.run_all",
                 
                 "custom_kcs.src.custom_fields.add_fields_contract_doctype.run_all",

                 "custom_kcs.src.custom_fields.create_contract_role_doctype.create_contract_role_doctype",

                 "custom_kcs.src.custom_fields.create_overtime_doctype.run_all",

                 "custom_kcs.src.custom_fields.add_fields_employee.run_all",	

                 "custom_kcs.src.custom_fields.add_fields_employee_attendance.add_fields_to_employee_attendance",

                 "custom_kcs.src.custom_fields.add_fields_branch.run_all",

                 "custom_kcs.src.custom_fields.create_employee_child_table.create_employee_child_table",

                 "custom_kcs.src.custom_fields.add_fields_employee_incentive.add_incentive_days_field",
                 
                 "custom_kcs.src.custom_fields.create_customer_branch_filter_doctype.run_all",
                 
                    "custom_kcs.src.custom_fields.add_fields_payroll_entry.run_all",
                    "custom_kcs.src.custom_fields.create_salary_paid_status_report.create_salary_paid_status_report",
                    "custom_kcs.src.custom_fields.create_shift_log_doctype.run_all",
                    "custom_kcs.src.custom_fields.add_fields_salary_slip.run_all",
                    "custom_kcs.src.custom_fields.create_mega_contract_doctype.run_all",
                    "custom_kcs.src.custom_fields.create_equipment_doctype.run_all",
                    "custom_kcs.src.custom_fields.attendance_status_doctype.run_all",
                    "custom_kcs.src.custom_fields.create_unit_doctype.run_all",
                    "custom_kcs.src.custom_fields.create_unit_costing_doctype.run_all",
                    "custom_kcs.src.custom_fields.create_minimum_wage_doctype.run_all",                
                ]   

boot_session = "custom_kcs.src.patches.override_monthly_attendance.boot"


# override_report = {
#     "HR": {
#         "Salary Paid Status": "custom_kcs.src.salary_paid_status"
#     }
# }
# override_doctype_class = {
#     "Payroll Entry": "custom_kcs.src.payroll_entry.PayrollEntry"
# }
# override_report = {
#     "HR": {
#         "Monthly Attendance Sheet": "custom_kcs.src.custom_reports.monthly_attendance_sheet"
#     }
# }

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "custom_kcs",
# 		"logo": "/assets/custom_kcs/logo.png",
# 		"title": "Custom Kcs",
# 		"route": "/custom_kcs",
# 		"has_permission": "custom_kcs.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------



# include js, css files in header of desk.html
# app_include_css = "/assets/custom_kcs/css/custom_kcs.css"
app_include_js = [
    "/assets/custom_kcs/js/payroll_entry.js",
    "/assets/custom_kcs/js/monthly_attendance_sheet.js",
    "/assets/custom_kcs/js/salary_paid_status.js",
    "/assets/custom_kcs/js/contract.js"
    ]

# query_reports = [
#     "Client Salary Report"
# ]
# include js, css files in header of web template
# web_include_css = "/assets/custom_kcs/css/custom_kcs.css"
# web_include_js = "/assets/custom_kcs/js/custom_kcs.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "custom_kcs/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Branch": "public/js/branch.js", 
              "Employee":"public/js/employee.js",
              "Employee Grade": "public/js/employee_grade.js",
              "Salary Structure Assignment": "public/js/salary_structure_assignment.js",
              "Contract": "public/js/contract.js",
              "Salary Structure": "public/js/salary_structure.js",
              "Employee Incentive":"public/js/employee_incentive.js",
            }


# override_report = {
#     "HR": {
#         "Monthly Attendance Sheet": "custom_kcs.custom_reports.monthly_attendance_sheet"
#     }
# }

# override_report_js = {
#     "Monthly Attendance Sheet": "custom_kcs/public/js/monthly_attendance_sheet.js"
# }
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "custom_kcs/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "custom_kcs.utils.jinja_methods",
# 	"filters": "custom_kcs.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "custom_kcs.install.before_install"
# after_install = "custom_kcs.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "custom_kcs.uninstall.before_uninstall"
# after_uninstall = "custom_kcs.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "custom_kcs.utils.before_app_install"
# after_app_install = "custom_kcs.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "custom_kcs.utils.before_app_uninstall"
# after_app_uninstall = "custom_kcs.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "custom_kcs.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

override_doctype_class = {
    "Attendance": "custom_kcs.src.overrides.custom_attendance.CustomAttendance",
    "Payroll Entry": "custom_kcs.src.payroll_entry.PayrollEntry",
    "Salary Slip": "custom_kcs.src.overrides.salary_slip.SalarySlip",
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }
# Scheduled Tasks
# ---------------

doc_events = {
    # "Employee Checkin": {
    #     "before_insert": "custom_kcs.src.before_insert_checkin.before_insert_checkin"
    # },
    "Attendance": {
        "before_insert": "custom_kcs.src.attendance_customization.validate_duplicate_attendance"
    },
    "Employee": {
        "validate": "custom_kcs.src.employee.validate_employee"
    },
     "Contract": {
        "on_submit": "custom_kcs.src.contract.on_contract_submit",
        "on_cancel": "custom_kcs.src.contract.clear_linked_contract",
        "after_insert": "custom_kcs.src.contract.update_mega_contract_links"
    },
    "Salary Slip": {
        "on_submit": [
              "custom_kcs.src.create_client_salary.create"
            ]         
    }
}

# override_whitelisted_methods = {
#     'custom_kcs.src.attendance_utils.get_employees_for_logged_in_manager': 'custom_kcs.src.attendance_utils.get_employees_for_logged_in_manager',
#     'custom_kcs.src.attendance_utils.mark_bulk_attendance': 'custom_kcs.src.attendance_utils.mark_bulk_attendance'
# }

scheduler_events = {
	"all": [
        "custom_kcs.src.cron.delete_old_attendance.delete_old_attendance_files"
	],
	"daily": [
		"custom_kcs.src.cron.send_contract_renewal_reminder.send_contract_renewal_reminder"
	],
	# "hourly": [
	# 	"custom_kcs.tasks.hourly"
	# ],
	# "weekly": [
	# 	"custom_kcs.tasks.weekly"
	# ],
	# "monthly": [
	# 	"custom_kcs.src.cron.generate_salary_slip.generate_salary_slip"
	# ],
    "cron": {
        "* * * * *": [ 
            "custom_kcs.src.cron.employee_Incentive.generate_employee_incentives_for_all"
        ]
    }
}

# Testing
# -------

# before_tests = "custom_kcs.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "custom_kcs.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "custom_kcs.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["custom_kcs.utils.before_request"]
# after_request = ["custom_kcs.utils.after_request"]

# Job Events
# ----------
# before_job = ["custom_kcs.utils.before_job"]
# after_job = ["custom_kcs.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"custom_kcs.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


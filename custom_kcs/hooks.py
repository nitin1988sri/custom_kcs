
app_name = "custom_kcs"
app_title = "Custom Kcs"
app_publisher = "saurabh srivastava"
app_description = "Custome code for kcs"
app_email = "saurabh.srivastava.mca@gmail.com"
app_license = "mit"

# Apps
# ------------------
after_migrate = ["custom_kcs.src.custom_fields.custom_field.create_employee_image_field",
                 "custom_kcs.src.custom_fields.create_contract_doctype.create_custom_fields",
                 "custom_kcs.src.custom_fields.create_contract_role_doctype.create_contract_role_doctype",
                 "custom_kcs.src.custom_fields.add_fields_to_branch.add_fields_to_branch",
                 "custom_kcs.src.custom_fields.create_temporary_transfer_doctype.create_temporary_transfer_doctype",
                 "custom_kcs.src.custom_fields.add_client_field_to_employee.add_client_field_to_employee",	
                 "custom_kcs.src.custom_fields.create_shift_log_doctype.create_shift_log_doctype",
                 "custom_kcs.src.custom_fields.add_fields_to_employee_checkin.add_fields_to_employee_checkin",
                 "custom_kcs.src.custom_fields.add_incentive_days_field_in_salary_slip.add_incentive_days_field_in_salary_slip",
                 "custom_kcs.src.custom_fields.add_fields_to_employee_attendance.add_fields_to_employee_attendance",
                 "custom_kcs.src.custom_fields.add_salary_structure_field.add_salary_structure_field",
                 "custom_kcs.src.custom_fields.add_client_field_to_branch.add_client_field_to_branch",
                 "custom_kcs.src.custom_fields.add_shift_field.add_shift_field",
                 "custom_kcs.src.delete_wrong_attendance.cancel_and_delete_all_attendance",
                 "custom_kcs.src.mark_bulk_attendance.mark_bulk_attendance"
                ]   

# required_apps = []

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
# app_include_js = "/assets/custom_kcs/js/custom_kcs.js"

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
doctype_js = {"Contract": "public/js/contract.js", 
              "Salary Slip":"public/js/salary_slip.js",
              "Employee":"public/js/employee.js",
              "Employee Grade": "public/js/employee_grade.js",
              "Salary Structure Assignment": "public/js/salary_structure_assignment.js"

}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
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
    "Attendance": "custom_kcs.src.overrides.custom_attendance.CustomAttendance"
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
    "Contract": {
        "before_save": "custom_kcs.src.contract.update_personnel_count",
        "before_insert": "custom_kcs.src.contract.before_insert"
    },
    "Employee Checkin": {
        "before_insert": "custom_kcs.src.before_insert_checkin.before_insert_checkin"
    },
    "Attendance": {
        "before_insert": "custom_kcs.src.attendance_customization.validate_duplicate_attendance"
    },
    "Salary Slip": {
        "before_save": "custom_kcs.src.custom_salary_slip.get_employee_attendance_data_on_save",
        "before_submit": "custom_kcs.src.custom_salary_slip.get_employee_attendance_data_on_save"
    },
    "Employee": {
        "validate": "custom_kcs.src.employee.validate_employee"
    }
}


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
	"monthly": [
		"custom_kcs.src.cron.generate_salary_slip.generate_salary_slip"
	],
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


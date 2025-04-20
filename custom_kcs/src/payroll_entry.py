# import frappe
# from frappe import _
# from hrms.payroll.doctype.payroll_entry.payroll_entry import (
#     PayrollEntry as CorePayrollEntry,
#     get_employee_list
# )
# import json


# class PayrollEntry(CorePayrollEntry):
#     def fill_employee_details(self):
#         filters = self.make_filters()

#         selected_branches_raw = self.get("selected_branches") or "[]"
#         selected_branches = json.loads(selected_branches_raw) 

#         self.set("employees", [])
#         employees = []

#         for branch in selected_branches:
#             filters.branch = branch
#             branch_employees = get_employee_list(filters=filters, as_dict=True, ignore_match_conditions=True)
#             employees.extend(branch_employees)

#         unique_employees = {e.employee: e for e in employees}.values()

#         if not unique_employees:
#             frappe.throw(_("No employees found for selected branches"))

#         self.set("employees", list(unique_employees))
#         self.number_of_employees = len(self.employees)
#         self.update_employees_with_withheld_salaries()

#         return self.get_employees_with_unmarked_attendance()
    
# def make_filters(self):
#     filters = frappe._dict(
#         company=self.company,
#         department=self.department,
#         designation=self.designation,
#         grade=self.grade,
#         currency=self.currency,
#         start_date=self.start_date,
#         end_date=self.end_date,
#         payroll_payable_account=self.payroll_payable_account,
#         salary_slip_based_on_timesheet=self.salary_slip_based_on_timesheet,
#     )

#     if not self.salary_slip_based_on_timesheet:
#         filters.update(dict(payroll_frequency=self.payroll_frequency))

#     return filters    


# @frappe.whitelist()
# def get_custom_employees(payroll_entry):
#     doc = frappe.get_doc("Payroll Entry", payroll_entry)
#     doc.fill_employee_details()
#     doc.save()


import frappe
from frappe import _
from hrms.payroll.doctype.payroll_entry.payroll_entry import (
    PayrollEntry as CorePayrollEntry,
    get_employee_list
)
import json

class PayrollEntry(CorePayrollEntry):
    def make_filters(self):
        filters = frappe._dict(
            company=self.company,
            department=self.department,
            designation=self.designation,
            grade=self.grade,
            currency=self.currency,
            start_date=self.start_date,
            end_date=self.end_date,
            payroll_payable_account=self.payroll_payable_account,
            salary_slip_based_on_timesheet=self.salary_slip_based_on_timesheet,
        )

        if not self.salary_slip_based_on_timesheet:
            filters.update(dict(payroll_frequency=self.payroll_frequency))

        return filters

    def fill_employee_details(self):
        filters = self.make_filters()

        selected_branches_raw = self.get("selected_branches") or "[]"
        selected_branches = json.loads(selected_branches_raw) 

        self.set("employees", [])
        employees = []

        for branch in selected_branches:
            filters.branch = branch
            branch_employees = get_employee_list(
                filters=filters,
                as_dict=True,
                ignore_match_conditions=True
            )
            employees.extend(branch_employees)

        unique_employees = {e.employee: e for e in employees}.values()

        if not unique_employees:
            frappe.throw(_("No employees found for selected branches"))

        self.set("employees", list(unique_employees))
        self.number_of_employees = len(self.employees)
        self.update_employees_with_withheld_salaries()

        return self.get_employees_with_unmarked_attendance()

@frappe.whitelist()
def get_custom_employees(payroll_entry):
    doc = frappe.get_doc("Payroll Entry", payroll_entry)
    doc.fill_employee_details()
    doc.save()

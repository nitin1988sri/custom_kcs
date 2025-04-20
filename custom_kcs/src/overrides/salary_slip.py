from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip as ERPNextSalarySlip

class SalarySlip(ERPNextSalarySlip):
    def check_existing(self):
        if str(self.is_client_slip) == "1":
            return  

        super().check_existing() 
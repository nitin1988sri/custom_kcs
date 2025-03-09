import frappe
from hrms.hr.doctype.attendance.attendance import Attendance

class CustomAttendance(Attendance):
    def validate_duplicate_record(self):
        """Override function to disable duplicate attendance validation"""
        pass 

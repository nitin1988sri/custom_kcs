import frappe
import secrets  
import string
from datetime import datetime, timedelta

def generate_random_password(length=8):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

def get_random_record(doctype, filters=None, field="name"):
    filters = filters or {}
    records = frappe.get_all(doctype, filters=filters, fields=[field])
    return secrets.choice(records)[field] if records else None 

def create_users_and_employees(count=5):
    """Creates multiple Users and their linked Employees"""

    first_names = [
    "Amit", "Saurabh", "Rajesh", "Vikram", "Neha", "Pooja", "Ravi", "Simran", "Kunal", "Anjali",
    "Arjun", "Rohan", "Mohit", "Deepak", "Vivek", "Sandeep", "Manish", "Nitin", "Harsh", "Rahul",
    "Yash", "Kapil", "Varun", "Prakash", "Suhas", "Tanmay", "Jay", "Shivam", "Siddharth", "Kartik",
    "Ishaan", "Ashish", "Gaurav", "Anup", "Madhav", "Sameer", "Aditya", "Abhishek", "Aniket", "Dev",
    "Tushar", "Ujjwal", "Omkar", "Suraj", "Ajay", "Nikhil", "Keshav", "Lakshya", "Chetan", "Dheeraj",
    "Anirudh", "Shankar", "Vinay", "Harshit", "Jatin", "Vishal", "Chirag", "Rajat", "Sagar", "Tarun",
    "Santosh", "Bhavesh", "Rakesh", "Satyam", "Parth", "Akhil", "Navneet", "Ravindra", "Bharat", "Anshul",
    "Devendra", "Pushkar", "Arnav", "Hardik", "Shubham", "Tejas", "Girish", "Piyush", "Mayank", "Dinesh",
    "Satyendra", "Harendra", "Hemant", "Pranav", "Vaibhav", "Yuvraj", "Soham", "Rishi", "Pratyush", "Samar",
    "Sumeet", "Uday", "Atul", "Ayaan", "Naveen", "Arvind", "Jignesh", "Rajeev", "Dhruv", "Kishore"
    ]       
    
    last_names = [
    "Sharma", "Verma", "Singh", "Yadav", "Mishra", "Gupta", "Agarwal", "Bansal", "Jain", "Trivedi",
    "Srivastava", "Chauhan", "Rathore", "Thakur", "Tiwari", "Dwivedi", "Chopra", "Kohli", "Malhotra", "Mehta",
    "Kumar", "Chaturvedi", "Shukla", "Pandey", "Choudhary", "Bhattacharya", "Basu", "Ghosh", "Patel", "Joshi",
    "Kulkarni", "Deshmukh", "Sawant", "Naik", "Shetty", "Iyengar", "Menon", "Nair", "Iyer", "Reddy",
    "Rao", "Krishnan", "Shastri", "Venkatesh", "Pillai", "Dutta", "Mitra", "Banerjee", "Sengupta", "Chakraborty",
    "Roy", "Das", "Mahapatra", "Behera", "Sahoo", "Swain", "Mohanty", "Tripathi", "Yadav", "Rajput",
    "Sisodia", "Gaur", "Tomar", "Dhillon", "Saini", "Sandhu", "Khatri", "Lamba", "Lal", "Bajpai",
    "Upadhyay", "Nigam", "Rawat", "Tyagi", "Bhargava", "Somani", "Mathur", "Sachdeva", "Bhandari", "Parikh",
    "Gandhi", "Choudhari", "Wadhwa", "Nagpal", "Madaan", "Vohra", "Chabra", "Arora", "Sethi", "Ahluwalia",
    "Bagga", "Sodhi", "Gagneja", "Talwar", "Juneja", "Saluja", "Saran", "Saxena", "Bhaskar", "Kashyap"
    ]

    for _ in range(count):
        first_name = secrets.choice(first_names)
        last_name = secrets.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}@example.com"
        password = generate_random_password()

        if frappe.db.exists("User", email):
            print(f"User {email} already exists! Skipping...")
            continue

        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "send_welcome_email": 0,
            "new_password": password,
            "roles": [{"role": "Employee"}]
        })
        user.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ User Created: {email} (Password: {password})")

        client = get_random_record("Customer")
        branch = get_random_record("Branch", filters={"client": client})
        shift = get_random_record("Shift Type")
        #allowed_designations = ["Cook", "Security guard", "Driver", "Superviser", "Gardener"]
        allowed_designations = ["Security guard"]

        designation = secrets.choice(allowed_designations)

        department = "Sales"
        grade = "D"
        gender = secrets.choice(["Male", "Female", "Other"])
        
        date_of_birth = datetime.today() - timedelta(days=secrets.randbelow(20000))  
        date_of_joining = datetime.today() - timedelta(days=secrets.randbelow(365))  

        if not client or not branch or not shift:
            print(f"❌ Missing data for Client, Branch, or Shift! Skipping user {email}...")
            continue

        employee = frappe.get_doc({
            "doctype": "Employee",
            "first_name": first_name,
            "last_name": last_name,
            "user_id": user.name,
            "company": "KCS",
            "client": client,
            "branch": branch,
            "shift": shift,
            "designation": designation,
            "department": department,
            "grade": grade,
            "employment_type": "Full-time",
            "gender": gender,
            "date_of_birth": date_of_birth.strftime('%Y-%m-%d'),
            "date_of_joining": date_of_joining.strftime('%Y-%m-%d'),
            "status": "Active"
        })
        employee.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Employee Created: {employee.name} linked to {user.name}")

def execute():
    create_users_and_employees(20)  

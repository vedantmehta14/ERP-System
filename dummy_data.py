# Run this command in terminal: python manage.py shell
# Then copy paste the below code

import random
import string
from emp_engagement.models import user_data
from django.utils import timezone
from faker import Faker

fake = Faker('en_IN')

# Hard-coded lists for names, positions, qualifications, and departments
first_names = ['Rajesh', 'Anil', 'Kiran', 'Vijay', 'Sunita', 'Priya', 'Rakesh', 'Manish', 'Nisha', 'Pooja', 'Amit', 'Neha', 'Ravi', 'Sonal', 'Ashok']
middle_names = ['Kumar', 'Rani', 'Devi', 'Prasad', 'Singh', 'Kaur', 'Rao', 'Bala', 'Nath', 'Patel', 'Lal', 'Das', 'Varma', 'Pal', 'Naik']
last_names = ['Sharma', 'Patel', 'Mehta', 'Gupta', 'Singh', 'Khan', 'Verma', 'Chopra', 'Bhatia', 'Joshi', 'Thakur', 'Desai', 'Gandhi', 'Kapoor', 'Mishra']
positions = ['Software Engineer', 'Data Scientist', 'Database Administrator', 'Network Engineer', 'System Analyst']
qualifications = ['B.Tech', 'M.Tech', 'BCA', 'MCA', 'B.Sc CS', 'M.Sc CS']
departments = ['Development', 'Data Analytics', 'Database Management', 'Network Operations', 'Systems Analysis']
indian_states = ['Maharashtra', 'Gujarat', 'Tamil Nadu', 'Karnataka', 'West Bengal', 'Rajasthan', 'Uttar Pradesh']
indian_cities = ['Mumbai', 'Ahmedabad', 'Chennai', 'Bangalore', 'Kolkata', 'Jaipur', 'Lucknow']

# Fetch specific users to be used for Reports To assignment
reports_to_users = ['Vejanand Chavda', 'Dhimant Patel', 'Pathik Patel']

# Ensuring no repetition in first names, middle names, and last names
used_first_names = set()
used_middle_names = set()
used_last_names = set()

for _ in range(11):  # Run only 11 times
    first_name = random.choice(first_names)
    while first_name in used_first_names:
        first_name = random.choice(first_names)
    used_first_names.add(first_name)

    middle_name = random.choice(middle_names)
    while middle_name in used_middle_names or middle_name == first_name:
        middle_name = random.choice(middle_names)
    used_middle_names.add(middle_name)

    last_name = random.choice(last_names)
    while last_name in used_last_names:
        last_name = random.choice(last_names)
    used_last_names.add(last_name)

    address1 = f"{random.randint(1, 100)}, {random.choice(indian_cities)}"
    address2 = f"{random.randint(101, 999)}, {random.choice(['Street', 'Lane', 'Avenue', 'Boulevard'])}"
    city = random.choice(indian_cities)
    state = random.choice(indian_states)
    pincode = ''.join(random.choices(string.digits, k=6))
    gender = random.choice(['M', 'F', 'O'])
    qualifications_choice = random.choice(qualifications)
    position_choice = random.choice(positions)
    department_choice = random.choice(departments)
    email = f"{first_name.lower()}.{last_name.lower()}_{random.randint(1000, 9999)}@example.com"  # Append random string
    phone_number = ''.join(random.choices(string.digits, k=10))
    salary = random.randint(20000, 250000)
    
    # Choose a random user as the Reports To for the current user
    report_to = random.choice(reports_to_users)
    
    # Generate Username (concatenating capitalized first name and last name)
    username = f"{first_name.capitalize()}{last_name.capitalize()}"

    user = user_data.objects.create(
        Username=username,
        FirstName=first_name,
        MiddleName=middle_name,
        LastName=last_name,
        Address1=address1,
        Address2=address2,
        City=city,
        State=state,
        Pincode=pincode,
        Country='India',
        DateofBirth=fake.date_of_birth(),
        Gender=gender,
        Qualifications=qualifications_choice,
        Position=position_choice,
        Department=department_choice,
        Reportsto=report_to,
        Email=email,
        Phone_number=phone_number,
        is_user=True,  # Set is_user to True
        Salary=salary
    )
    user.save()


from django.db import models

# Create your models here.
class user_credentials(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=15)

    def __str__(self):
        return self.username
    
    
class user_data(models.Model):
    Username= models.CharField(max_length=30)
    Password= models.CharField(default="admin123",max_length=15)
    FirstName= models.CharField(max_length=100)
    MiddleName= models.CharField(max_length=100, blank=True)
    LastName = models.CharField(max_length=100)
    Address1= models.CharField(max_length=50)
    Address2= models.CharField(max_length=50)
    City= models.CharField(max_length=50)
    State= models.CharField(max_length=50)
    Pincode= models.CharField(max_length=10)
    Country= models.CharField(max_length=50)
    DateofBirth= models.DateField()
    Gender_choices=(
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    Gender= models.CharField(max_length=1, choices=Gender_choices)
    Qualifications = models.CharField(max_length=255)
    Position = models.CharField(max_length=100)
    Department = models.CharField(max_length=100)
    Reportsto= models.CharField(max_length=50,default= None)
    Email = models.EmailField(unique=True)
    Phone_number = models.CharField(max_length=15)
    is_user = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    Profilepic = models.ImageField(default='default_male_pic.png', upload_to='profile_pics/', blank=True, null=True)
    Salary = models.IntegerField(default=0)
    
    def __str__(self):
        return self.Username


class Event(models.Model):
    eventid = models.CharField(max_length=6)
    username = models.CharField(max_length=30)
    title = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    details = models.TextField()

    def _str_(self):
        return self.title

class TimeSheetData(models.Model):
    username = models.CharField(max_length=30)
    date = models.DateField(auto_now_add=True)
    check_in_time = models.TimeField(null=True,blank=True)
    check_out_time = models.TimeField(null=True,blank=True)
    total_time = models.CharField(max_length=8, default='')

    def str(self):
        return self.username

class Holidays(models.Model):
    username = models.CharField(max_length=30)
    holidayid = models.CharField(max_length=6)
    title = models.CharField(max_length=30)
    date = models.DateField()
    day = models.CharField(max_length=15)

    def str(self):
        return self.title

class Leave(models.Model):
    LEAVE_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Not Approved', 'Not Approved'),
    ]

    username = models.CharField(max_length=30)
    emp_name = models.CharField(max_length=30, blank=True)
    leave_id = models.CharField(max_length=6)
    start_date = models.DateField()
    end_date = models.DateField()
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=LEAVE_STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Leave {self.subject} for {self.username}"

class Announcement(models.Model):
    username = models.CharField(max_length=30)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.content[:20]}"
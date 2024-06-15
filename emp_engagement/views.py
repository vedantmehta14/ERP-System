from django.utils import timezone
from django.utils.timezone import now
import uuid
from emp_engagement.models import user_credentials, user_data, Event, TimeSheetData, Holidays, Leave, Announcement
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .decorators import login_access_only, isUser
import datetime
from . import urls
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import calendar
import random
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def login_page(request):
    return render(request, 'login.html')

def login_user(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        # print("Username: ",username)
        # print("Password: ",password)
        try:
            user= user_data.objects.get(Username=username)
            # print(user)
            # print(user.is_user)
            # print(user.is_admin)
            if user.Password == password and (user.is_user== True or user.is_admin== True):

                timezone.activate("Asia/Kolkata")
                TimeSheetData.objects.create(username=username, check_in_time=timezone.localtime(timezone.now()))

                display_name= user.FirstName + " " + user.LastName
                quali= user.Qualifications
                profile_pic_url= user.Profilepic.url
                request.session['username'] = username
                request.session['password'] = password
                request.session['firstname']= user.FirstName
                request.session['middlename']= user.MiddleName
                request.session['lastname']= user.LastName
                request.session['display_name']= display_name
                request.session['address1']= user.Address1
                request.session['address2']= user.Address2
                request.session['city']= user.City
                request.session['state']= user.State
                request.session['country']= user.Country
                request.session['pincode']= user.Pincode
                request.session['dob']= user.DateofBirth.strftime('%Y-%m-%d')
                request.session['salary']=user.Salary
                if user.Gender == 'M':
                    request.session['gender']= "Male"
                elif user.Gender == 'F':
                    request.session['gender'] = "Female"
                else:
                    request.session['gender']= "Others"
                if user.is_admin:
                    menu_list= urls.AdminMenulist
                elif user.is_user:
                    menu_list= urls.UserMenulist
                else:
                    menu_list= None 
                # print(menu_list)
                request.session['menu_list']=menu_list
                request.session['quali']=quali
                request.session['position']= user.Position
                request.session['department']= user.Department
                request.session['reports']= user.Reportsto
                request.session['email']= user.Email
                request.session['phone_number']= user.Phone_number
                request.session['profile_pic_url']=profile_pic_url
                request.session['is_user']=user.is_user
                request.session['is_admin']=user.is_admin
                # print(profile_pic_url)
                messages.success(request,"Successfully logged in!")
                # print("User logged in",user)
                # Commented out the below line because when index is rendered the url does not change. the page needs to be redirected
                # return render(request,'index.html',{'display_name': display_name, 'position':user.Position, 'profile_pic_url':profile_pic_url, 'menu_list':menu_list})
                return redirect('dashboard')
            else :
                messages.error(request,"Check Credentials")
                return render(request,'login.html')

        except user_data.DoesNotExist:
            messages.error(request, "Invalid username")
            return redirect("/login")
            
    return render(request,'login.html')

def register_user(request): 
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        firstname=request.POST.get('fname')
        middlename=request.POST.get('mname')
        lastname=request.POST.get('lname')
        address1=request.POST.get('address1')
        address2= request.POST.get('address2')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        country=request.POST.get('country')
        dateofbirth=request.POST.get('dob')
        gender=request.POST.get('gender')
        salary=request.POST.get('salary')
        qualification=request.POST.get('qualification')
        position=request.POST.get('position')
        department=request.POST.get('department')
        reportsto=request.POST.get('reportsto')
        email=request.POST.get('email')
        phonenumber=request.POST.get('phno')
        profilepic = request.FILES.get('profilepic') 
        # print(profilepic)
        if profilepic == None and gender=="M":
            profilepic="profile_pics/default_male_pic.png"
        elif profilepic == None and gender == "F":
            profilepic = "profile_pics/default_female_pic.png" 
        if password == "":
            password="admin123"
        # print(username)
        # print(password)
        # print(firstname)
        # print(middlename)
        # print(lastname)
        # print(profilepic)
        USERDATA = user_data.objects.create(
            Username=username,
            Password=password,
            FirstName= firstname,
            MiddleName= middlename,
            LastName= lastname,
            Address1= address1,
            Address2= address2,
            City= city,
            State= state,
            Pincode= pincode,
            Country = country,
            DateofBirth= dateofbirth,
            Gender= gender,
            Salary=salary,
            Qualifications= qualification,
            Position = position,
            Department = department,
            Reportsto = reportsto,
            Email= email,
            Phone_number= phonenumber,
            Profilepic = profilepic
            )
        # print(user)
        USERDATA.save()
        return render(request,'login.html')
        
                 
    return render(request,'register.html')

@login_access_only
def logout_user(request):
    timezone.activate("Asia/Kolkata")
    username = request.session.get('username')
    last_entry = TimeSheetData.objects.filter(username=username).order_by('-date', '-check_in_time').first()
    if last_entry:
        last_entry.check_out_time = timezone.localtime(timezone.now()).time()

        t1 = last_entry.check_in_time
        t2 = last_entry.check_out_time

        t1_seconds = t1.hour * 3600 + t1.minute * 60 + t1.second
        t2_seconds = t2.hour * 3600 + t2.minute * 60 + t2.second

        difference_seconds = t2_seconds - t1_seconds

        hours = difference_seconds // 3600
        minutes = (difference_seconds % 3600) // 60
        seconds = difference_seconds % 60

        time_diff = datetime.time(hour=hours, minute=minutes, second=seconds)

        last_entry.total_time = time_diff.strftime("%H:%M:%S")
        last_entry.save()

    logout(request)
    messages.info(request, "Logged out Successfully!")
    return redirect('/login')

@csrf_exempt
@login_access_only
def update_checkout_time(request):
    timezone.activate("Asia/Kolkata")
    username = request.session.get('username')
    if username:
        last_entry = TimeSheetData.objects.filter(username=username).order_by('-date', '-check_in_time').first()
        if last_entry and not last_entry.check_out_time:
            last_entry.check_out_time = timezone.localtime(timezone.now()).time()

            t1 = last_entry.check_in_time
            t2 = last_entry.check_out_time

            t1_seconds = t1.hour * 3600 + t1.minute * 60 + t1.second
            t2_seconds = t2.hour * 3600 + t2.minute * 60 + t2.second

            difference_seconds = t2_seconds - t1_seconds

            hours = difference_seconds // 3600
            minutes = (difference_seconds % 3600) // 60
            seconds = difference_seconds % 60

            time_diff = datetime.time(hour=hours, minute=minutes, second=seconds)

            last_entry.total_time = time_diff.strftime("%H:%M:%S")
            last_entry.save()

    return JsonResponse({'status': 'success'})

@login_access_only
def index(request): 
    #user= user_data.objects.get(Username=request.session.Username)
    dob_str = request.session.get('dob')
    date_of_birth = timezone.datetime.strptime(dob_str, '%Y-%m-%d').date()
    context = {
        'username': request.session.get('username'),
        'password': request.session.get('password'),
        'firstname': request.session.get('firstname'),
        'middlename': request.session.get('middlename'),
        'lastname': request.session.get('lastname'),
        'address1': request.session.get('address1'),
        'address2': request.session.get('address2'),
        'city': request.session.get('city'),
        'state': request.session.get('state'),
        'pincode': request.session.get('pincode'),
        'country': request.session.get('country'),
        'dob': date_of_birth,
        'gender': request.session.get('gender'),
        'salary': request.session.get('salary'),
        'quali': request.session.get('quali'),
        'position': request.session.get('position'),
        'department': request.session.get('department'),
        'reports': request.session.get('reports'),
        'email': request.session.get('email'),
        'phone_number': request.session.get('phone_number'),
        'profile_pic_url': request.session.get('profile_pic_url'),
        'display_name':request.session.get('display_name'),
        'menu_list': request.session.get('menu_list'),
        'is_user': request.session.get('is_user'),
        'is_admin':request.session.get('is_admin')
    }
    # print(request.session.get('reports'))
    return render(request,'index.html',context)

@login_access_only
def home(request): 
    display_name= request.session.get('display_name')
    position = request.session.get('position')
    profile_pic_url = request.session.get('profile_pic_url')
    menu_list= request.session.get('menu_list')
    return render(request,'home.html',{'display_name': display_name, 'position':position, 'profile_pic_url':profile_pic_url, 'menu_list':menu_list})

@login_access_only
def dashboard(request): 
    display_name= request.session.get('display_name')
    position = request.session.get('position')
    profile_pic_url = request.session.get('profile_pic_url')
    menu_list= request.session.get('menu_list')
    isAdmin = request.session.get('is_admin')
    announcements = Announcement.objects.all().order_by('-timestamp')
    events = Event.objects.all()
    event_data = Event.objects.filter(username=request.session.get('username'))
    current_month = now().month
    if isAdmin:
        timesheet_data = TimeSheetData.objects.order_by('-date', '-check_in_time')[1:6]
    else:
        timesheet_data = TimeSheetData.objects.filter(username=request.session.get('username')).order_by('-date', '-check_in_time')[1:6]
    birthday_users = user_data.objects.filter(DateofBirth__month=current_month)
    # birthday_users = user_data.objects.filter(DateofBirth__month=1)
    return render(request,'dashboard.html', {
        'display_name': display_name, 
        'position':position, 
        'profile_pic_url':profile_pic_url, 
        'menu_list':menu_list,
        'isAdmin': isAdmin,
        'announcements': announcements,
        'birthday_users': birthday_users,
        'timesheet_data': timesheet_data,
        'events': event_data
        })

@login_access_only
def add_announcement(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        currentUser = request.session.get('username')
        Announcement.objects.create(username=currentUser, content=content)
    return redirect('dashboard')

@login_access_only
def delete_announcement(request, announcement_id):
    if request.method == 'POST':
        announcement = get_object_or_404(Announcement, id=announcement_id)
        announcement.delete()
    return redirect('dashboard')

@login_access_only
def adminuser(request):
    users = user_data.objects.all()
    users_with_status = []

    for user in users:
        if user.is_admin:
            role = "Admin"
        elif user.is_user:
            role = "User"
        else:
            role = "None"
        
        status = "Inactive" if not user.is_user and not user.is_admin else "Active"
        users_with_status.append({
            'Username': user.Username,
            'FirstName': user.FirstName,
            'LastName': user.LastName,
            'Position': user.Position,
            'Department': user.Department,
            'Reportsto': user.Reportsto,
            'status': status,
            'pic_url': user.Profilepic,
            'role': role
        })

    context = {
        'users': users_with_status,
        'is_admin': request.session.get('is_admin'),
        'is_user': request.session.get('is_user'),
        'display_name': request.session.get('display_name'),
        'position': request.session.get('position'),
        'profile_pic_url': request.session.get('profile_pic_url'),
        'menu_list': request.session.get('menu_list')
    }
    return render(request, 'adminuser.html', context)

def get_user_details(request, username):
    user = get_object_or_404(user_data, Username=username)
    data = {
        'Username': user.Username,
        'Password': user.Password,
        'FirstName': user.FirstName,
        'MiddleName': user.MiddleName,
        'LastName': user.LastName,
        'DateofBirth': user.DateofBirth,
        'Qualifications': user.Qualifications,
        'Position': user.Position,
        'Department': user.Department,
        'Reportsto': user.Reportsto,
        'Email': user.Email,
        'Phone_number': user.Phone_number,
        'is_user': user.is_user,
        'is_admin': user.is_admin,
        'Salary': user.Salary,
        'pic_url': user.Profilepic.url,
    }
    return JsonResponse(data)

def edit_user(request):
    if request.method == 'POST':
        username = request.POST['Username']
        user = get_object_or_404(user_data, Username=username)
        user.Password = request.POST['Password']
        user.FirstName = request.POST['FirstName']
        user.MiddleName = request.POST['MiddleName']
        user.LastName = request.POST['LastName']
        user.DateofBirth = request.POST['DateofBirth']
        user.Qualifications = request.POST['Qualifications']
        user.Position = request.POST['Position']
        user.Department = request.POST['Department']
        user.Reportsto = request.POST['Reportsto']
        user.Email = request.POST['Email']
        user.Phone_number = request.POST['Phone_number']
        user.is_user = request.POST['is_user'] == 'True'
        user.is_admin = request.POST['is_admin'] == 'True'
        user.Salary = request.POST['Salary']
        user.save()
        return HttpResponseRedirect(reverse('adminuser'))

def delete_user(request,username):
    user= user_data.objects.get(Username=username)
    user.delete()
    return redirect('/adminuser')
    
@login_access_only
def user(request): 
    dob_str = request.session.get('dob')
    date_of_birth = timezone.datetime.strptime(dob_str, '%Y-%m-%d').date()
    context = {
        'username': request.session.get('username'),
        'password': request.session.get('password'),
        'firstname': request.session.get('firstname'),
        'middlename': request.session.get('middlename'),
        'lastname': request.session.get('lastname'),
        'address1': request.session.get('address1'),
        'address2': request.session.get('address2'),
        'city': request.session.get('city'),
        'state': request.session.get('state'),
        'pincode': request.session.get('pincode'),
        'country': request.session.get('country'),
        'dob': date_of_birth,
        'gender': request.session.get('gender'),
        'quali': request.session.get('quali'),
        'position': request.session.get('position'),
        'department': request.session.get('department'),
        'reports': request.session.get('reports'),
        'email': request.session.get('email'),
        'phone_number': request.session.get('phone_number'),
        'profile_pic_url': request.session.get('profile_pic_url'),
        'display_name':request.session.get('display_name'),
        'menu_list': request.session.get('menu_list'),
        'is_user': request.session.get('is_user'),
        'is_admin':request.session.get('is_admin')
    }
    if request.method =="POST":
        if 'passwordChange' in request.POST:
            currentUser = request.session.get('username')
            password = request.session.get('password')
            currentPassword = request.POST.get("currentPassword")
            newPassword= request.POST.get("newPassword")
            confirmPassword = request.POST.get("confirmPassword")
            if password == currentPassword:
                if newPassword != currentPassword:
                    if newPassword == confirmPassword:
                        # print("Successfull")
                        user= user_data.objects.get(Username=currentUser)
                        user.Password = newPassword
                        user.save()
                        #user.user_data.save()
                        request.session['password'] = newPassword
                        context = {
                        'username': request.session.get('username'),
                        'password': request.session.get('password'),
                        'firstname': request.session.get('firstname'),
                        'middlename': request.session.get('middlename'),
                        'lastname': request.session.get('lastname'),
                        'address1': request.session.get('address1'),
                        'address2': request.session.get('address2'),
                        'city': request.session.get('city'),
                        'state': request.session.get('state'),
                        'pincode': request.session.get('pincode'),
                        'country': request.session.get('country'),
                        'dob': date_of_birth,
                        'gender': request.session.get('gender'),
                        'quali': request.session.get('quali'),
                        'position': request.session.get('position'),
                        'department': request.session.get('department'),
                        'reports': request.session.get('reports'),
                        'email': request.session.get('email'),
                        'phone_number': request.session.get('phone_number'),
                        'profile_pic_url': request.session.get('profile_pic_url'),
                        'display_name':request.session.get('display_name'),
                        'menu_list': request.session.get('menu_list')
                        }
                        return render(request, 'user.html', context)    
                    else:
                        print("passwords dont match")
                else:
                    print("password is same as previous password")
            else:
                print("current password does not match")    
        
        if 'addressChange' in request.POST:
            currentUser = request.session.get('username')
            newAddress1 = request.POST.get('new_address_line_1')
            newAddress2 = request.POST.get('new_address_line_2')
            newCity = request.POST.get('new_city')
            newPincode = request.POST.get('new_pincode')
            newState = request.POST.get('new_state')
            newCountry = request.POST.get('new_country')
            user= user_data.objects.get(Username=currentUser)
            user.Address1 = newAddress1
            user.Address2 = newAddress2
            user.City= newCity
            user.Pincode= newPincode
            user.State= newState
            user.Country= newCountry
            user.save()
            request.session['address1']= newAddress1
            request.session['address2']= newAddress2
            request.session['city']= newCity
            request.session['pincode']= newPincode
            request.session['state']= newState
            request.session['country']= newCountry
            context = {
            'username': request.session.get('username'),
            'password': request.session.get('password'),
            'firstname': request.session.get('firstname'),
            'middlename': request.session.get('middlename'),
            'lastname': request.session.get('lastname'),
            'address1': request.session.get('address1'),
            'address2': request.session.get('address2'),
            'city': request.session.get('city'),
            'state': request.session.get('state'),
            'pincode': request.session.get('pincode'),
            'country': request.session.get('country'),
            'dob': date_of_birth,
            'gender': request.session.get('gender'),
            'quali': request.session.get('quali'),
            'position': request.session.get('position'),
            'department': request.session.get('department'),
            'reports': request.session.get('reports'),
            'email': request.session.get('email'),
            'phone_number': request.session.get('phone_number'),
            'profile_pic_url': request.session.get('profile_pic_url'),
            'display_name':request.session.get('display_name'),
            'menu_list': request.session.get('menu_list'),
            'is_user': request.session.get('is_user'),
            'is_admin':request.session.get('is_admin')
            }
            return render(request,'user.html',context)
        
        if 'profilepicChange' in request.POST:
            # print("Hello")
            currentUser= request.session.get('username')
            newprofileurl= request.FILES.get('newprofilepic')
            user= user_data.objects.get(Username= currentUser)
            user.Profilepic= newprofileurl
            # print(newprofileurl)
            user.save()
            user= user_data.objects.get(Username= currentUser)
            newurl= user.Profilepic.url
            # print(newurl)
            request.session['profile_pic_url']= newurl
            context = {
            'username': request.session.get('username'),
            'password': request.session.get('password'),
            'firstname': request.session.get('firstname'),
            'middlename': request.session.get('middlename'),
            'lastname': request.session.get('lastname'),
            'address1': request.session.get('address1'),
            'address2': request.session.get('address2'),
            'city': request.session.get('city'),
            'state': request.session.get('state'),
            'pincode': request.session.get('pincode'),
            'country': request.session.get('country'),
            'dob': date_of_birth,
            'gender': request.session.get('gender'),
            'quali': request.session.get('quali'),
            'position': request.session.get('position'),
            'department': request.session.get('department'),
            'reports': request.session.get('reports'),
            'email': request.session.get('email'),
            'phone_number': request.session.get('phone_number'),
            'profile_pic_url': request.session.get('profile_pic_url'),
            'display_name':request.session.get('display_name'),
            'menu_list': request.session.get('menu_list'),
            'is_user': request.session.get('is_user'),
            'is_admin':request.session.get('is_admin')
            }
            return render(request,'user.html',context)
    return render(request,'user.html',context)

@login_access_only
def event(request): 
    currentUser = request.session.get('username')
    display_name = request.session.get('display_name')
    position = request.session.get('position')
    profile_pic_url = request.session.get('profile_pic_url')
    menu_list = request.session.get('menu_list')

    if request.method == 'POST':
        current_user = currentUser
        action = request.POST.get('action')  # Get the action (add, edit, or delete)
        event_id = request.POST.get('event-id')  # Get event ID for edit or delete

        if action == 'add':
            event_id = str(uuid.uuid4())[:6]
            title = request.POST.get('event-title')
            start = request.POST.get('event-start')
            end = request.POST.get('event-end')
            details = request.POST.get('event-details')

            # Create a new event
            Event.objects.create(
                eventid=event_id,
                username=current_user,
                title=title,
                start=start,
                end=end,
                details=details
            )

        elif action == 'edit':
            title = request.POST.get('event-title')
            start = request.POST.get('event-start')
            end = request.POST.get('event-end')
            details = request.POST.get('event-details')

            # Update the existing event
            event = Event.objects.get(eventid=event_id)
            event.title = title
            event.start = start
            event.end = end
            event.details = details
            event.save()

        elif action == 'delete':
            # Delete the event
            event = get_object_or_404(Event, eventid=event_id)  # Use eventid instead of id
            event.delete()

        return redirect('event')

    else:
        events = Event.objects.all()
        event_data = Event.objects.filter(username=request.session.get('username'))
        return render(request, 'event.html', {
            'display_name': display_name,
            'position': position,
            'profile_pic_url': profile_pic_url,
            'events': event_data,
            'menu_list': menu_list
        })

@login_access_only
def task(request): 
    display_name= request.session.get('display_name')
    position = request.session.get('position')
    profile_pic_url = request.session.get('profile_pic_url')
    menu_list = request.session.get('menu_list')
    return render(request,'task.html',{'display_name': display_name, 'position':position, 'profile_pic_url':profile_pic_url, 'menu_list':menu_list})

@login_access_only
def timesheet(request):
    display_name= request.session.get('display_name')
    position = request.session.get('position')
    profile_pic_url = request.session.get('profile_pic_url') 
    menu_list= request.session.get('menu_list')
    isAdmin = request.session.get('is_admin')
    if isAdmin:
        timesheet_data = TimeSheetData.objects.order_by('-date', '-check_in_time')[1:]
    else:
        timesheet_data = TimeSheetData.objects.filter(username=request.session.get('username')).order_by('-date', '-check_in_time')[1:]
      
    return render(request,'timesheet.html', {
        'display_name': display_name, 
        'position':position, 
        'profile_pic_url':profile_pic_url,
        'timesheet_data': timesheet_data, 
        'menu_list': menu_list,
        'isAdmin': isAdmin
        })

@login_access_only
def leave(request): 
    isAdmin = request.session.get('is_admin')
    currentUser = request.session.get('username')
    display_name= request.session.get('display_name')
    position = request.session.get('position')
    profile_pic_url = request.session.get('profile_pic_url')
    menu_list= request.session.get('menu_list')
    
    if request.method == 'POST':
        leave_id = str(uuid.uuid4())[:6]
        start_date = request.POST.get('leave_Startdate')
        end_date = request.POST.get('leave_Enddate')
        subject = request.POST.get('subject')

        Leave.objects.create(
            leave_id=leave_id,
            emp_name=display_name,
            username=currentUser,
            start_date=start_date,
            end_date=end_date,
            subject=subject,
            status='Pending'  # Default status
        )
        return redirect('leave')  # Redirect to the same page or any other page

    leave_records = Leave.objects.filter(username=currentUser).order_by('-start_date') if not isAdmin else Leave.objects.all().order_by('-start_date')

    return render(request, 'leave.html', {
        'display_name': display_name,
        'position': position,
        'profile_pic_url': profile_pic_url,
        'menu_list': menu_list,
        'leave_records': leave_records,
        'isAdmin': isAdmin
    })

@login_access_only
def approve_leave(request, leave_id):
    if not request.session.get('is_admin'):
        return HttpResponseForbidden()

    leave_record = get_object_or_404(Leave, leave_id=leave_id)
    leave_record.status = 'Approved'
    leave_record.save()
    return redirect('leave')

@login_access_only
def reject_leave(request, leave_id):
    if not request.session.get('is_admin'):
        return HttpResponseForbidden()

    leave_record = get_object_or_404(Leave, leave_id=leave_id)
    leave_record.status = 'Not Approved'
    leave_record.save()
    return redirect('leave')

@login_access_only
def manageadmin(request): 
    display_name= request.session.get('display_name')
    position = request.session.get('position')
    profile_pic_url = request.session.get('profile_pic_url')
    menu_list= request.session.get('menu_list')
    return render(request,'admin.html',{'display_name': display_name, 'position':position, 'profile_pic_url':profile_pic_url, 'menu_list': menu_list})

@login_access_only
def activeusers(request): 
    display_name= request.session.get('display_name')
    position = request.session.get('position')
    profile_pic_url = request.session.get('profile_pic_url')
    menu_list= request.session.get('menu_list')
    return render(request,'activeusers.html',{'display_name': display_name, 'position':position, 'profile_pic_url':profile_pic_url, 'menu_list': menu_list})

@login_access_only
def companypolicy(request): 
    display_name= request.session.get('display_name')
    position = request.session.get('position')
    profile_pic_url = request.session.get('profile_pic_url')
    menu_list= request.session.get('menu_list')
    return render(request,'policy.html',{'display_name': display_name, 'position':position, 'profile_pic_url':profile_pic_url, 'menu_list': menu_list})

@login_access_only
def checkinout(request): 
    display_name= request.session.get('display_name')
    position = request.session.get('position')
    profile_pic_url = request.session.get('profile_pic_url')
    menu_list= request.session.get('menu_list')
    return render(request,'checkinout.html',{'display_name': display_name, 'position':position, 'profile_pic_url':profile_pic_url, 'menu_list': menu_list})

@login_access_only
def holidays(request): 
    currentUser = request.session.get('username')
    display_name= request.session.get('display_name')
    position = request.session.get('position')
    profile_pic_url = request.session.get('profile_pic_url')
    menu_list = request.session.get('menu_list')
    isAdmin = request.session.get('is_admin')

    if request.method == 'POST':
        current_user = currentUser
        holiday_id = str(uuid.uuid4())[:6]
        title = request.POST.get('title')
        date = request.POST.get('date')
        date_object = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        day = date_object.strftime("%A") 

        holiday = Holidays.objects.create(
            username=current_user,
            holidayid=holiday_id,
            title=title,
            date=date,
            day=day,
        )
        holiday.save()
        
        return redirect('holidays')

    else:
        holiday_data = Holidays.objects.all()
        return render(request, 'holidays.html', {
            'display_name': display_name, 
            'position': position, 
            'profile_pic_url': profile_pic_url, 
            'holiday_data': holiday_data, 
            'menu_list': menu_list, 
            'isAdmin': isAdmin
        })

@login_access_only
def delete_holiday(request, holiday_id):
    holiday = get_object_or_404(Holidays, holidayid=holiday_id)
    holiday.delete()
    return redirect('holidays')

@login_access_only
def birthday(request): 
    display_name= request.session.get('display_name')
    position = request.session.get('position')
    profile_pic_url = request.session.get('profile_pic_url')
    menu_list= request.session.get('menu_list')
    return render(request,'birthday.html',{'display_name': display_name, 'position':position, 'profile_pic_url':profile_pic_url, 'menu_list': menu_list})

@login_access_only
def payslip(request): 
    display_name= request.session.get('display_name')
    position = request.session.get('position')
    profile_pic_url = request.session.get('profile_pic_url')
    menu_list = request.session.get('menu_list')

    if request.method == 'POST':
        year = request.POST.get('year')
        month = request.POST.get('month')

        # Fetching the required session details
        username = request.session.get('username')
        full_name = request.session.get('firstname')+' '+request.session.get('middlename')+' '+request.session.get('lastname')
        address_line_1 = request.session.get('address1')
        address_line_2 = request.session.get('address2')
        city = request.session.get('city')
        state = request.session.get('state')
        country = request.session.get('country')
        pincode = request.session.get('pincode')
        basic_salary = request.session.get('salary')
        department = request.session.get('department')
        email = request.session.get('email')
        phone_number = request.session.get('phone_number')

        # Generating random account number
        bank_codes = ["ABC", "DEF", "GHI"]
        branch_codes = ["1234", "5678", "9012"]
        bank_code = random.choice(bank_codes)
        branch_code = random.choice(branch_codes)
        account_number = ''.join(random.choices('0123456789', k=10))
        bank_account_number = bank_code+branch_code+account_number

        date_obj = datetime.datetime.strptime(month, "%B")
        month_number = date_obj.month

        response = HttpResponse(content_type='application/pdf')
        pdf_name = f'{month}_{year}.pdf'
        response['Content-Disposition'] = f'attachment; filename="{pdf_name}"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        styles = getSampleStyleSheet()

        company_logo = 'static/img/techsture_icon.webp' 
        company_name = 'Techsture Technologies Private Limited'
        company_address = '601, Avdhesh House, SG Highway, Bodakdev, Ahmedabad, Gujarat, India 380054'
        company_contact = 'Phone: +91 9033057219 / +91 9033067219 / +079 66610963'
        company_email = 'Email: info@techsture.com'
        corporate_identification_number_and_registration_number = 'CIN: U72900GJ2007PTC051730, Registration Number: 51730'
        # registration_number = 'Registration Number: 51730'

        payslip_content = []

        logo = Image(company_logo)
        logo.drawHeight = 25 
        logo.drawWidth = 25 

        logo_table = Table([[logo, Paragraph(company_name, styles['Heading1'])]], colWidths=[60, '*'], hAlign='CENTER')
        logo_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12)]))

        payslip_content.append(logo_table)

        center_style = ParagraphStyle(name='Center', alignment=1, fontName='Helvetica')
        payslip_content.append(Paragraph(company_address, center_style))
        payslip_content.append(Paragraph(company_contact, center_style))
        payslip_content.append(Paragraph(corporate_identification_number_and_registration_number, center_style))

        payslip_content.append(Spacer(1, 12))
        payslip_content.append(Paragraph('Pay Slip', styles['Title']))
        payslip_content.append(Paragraph('Employee Information',styles['Heading2']))
        data = [
            [Paragraph(f'Name: {full_name}', styles['Normal']), Paragraph(f'Username: {username}', styles['Normal'])],
            [Paragraph(f'Phone number: {phone_number}', styles['Normal']), Paragraph(f'Email: {email}', styles['Normal'])],
            [Paragraph(f'Position: {position}', styles['Normal']), Paragraph(f'Department: {department}', styles['Normal'])],
        ]
        table = Table(data, colWidths=[234, 234], hAlign='CENTER')
        table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONT', (0, 0), (-1, 0), 'Helvetica')]))
        payslip_content.append(table)
        payslip_content.append(Paragraph(f'Address: {address_line_1}, {address_line_2}, {city}, {state}, {country} {pincode}', styles['Normal']))       

        num_days_in_month = calendar.monthrange(int(year), int(month_number))[1]
        payslip_content.append(Paragraph('Payment Details', styles['Heading2']))
        payslip_content.append(Paragraph(f'Pay Period: {month} 1, {year} - {month} {num_days_in_month}, {year}', styles['Normal']))
        payslip_content.append(Paragraph('Daily Working Hours: 9', styles['Normal']))
        payslip_content.append(Paragraph(f'Pay Date: {month} {num_days_in_month}, {year}', styles['Normal']))
        payslip_content.append(Paragraph(f'Bank Account Number: {bank_account_number}', styles['Normal']))
        
        housing_allowance_percentage = 0.3  # 30% of the basic salary
        transport_allowance_percentage = 0.05  # 5% of the basic salary
        health_insurance_amount = 2000  # Health insurance premium
        pension_contribution_percentage = 0.1 # 10% of the basic salary
        income_tax_percentage = 0.2 # 20% of the basic salary

        housing_allowance = basic_salary * housing_allowance_percentage
        transport_allowance = basic_salary * transport_allowance_percentage

        payslip_content.append(Paragraph('Salary Breakdown', styles['Heading2']))
        data = [
            ['Earnings', 'Amount'],
            ['Basic', basic_salary],
            ['Housing Allowance', housing_allowance],
            ['Transport Allowance', transport_allowance]
        ]
        table = Table(data, colWidths=[230, 230], hAlign='CENTER')
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),
            ('LINEABOVE', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),
            ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.black) 
        ]))
        payslip_content.append(table)
        payslip_content.append(Spacer(1, 12))

        pension_contribution = basic_salary * pension_contribution_percentage

        def calculate_income_tax(basic_salary, health_insurance_amount, pension_contribution):

            taxable_income = basic_salary - health_insurance_amount - pension_contribution

            tax_slabs = [(0, 0.05), (500000, 0.1), (1000000, 0.2), (1500000, 0.3)]  # Example tax slabs
            tax_amount = 0

            # Calculate tax based on slabs
            for slab, rate in tax_slabs:
                if taxable_income > slab:
                    tax_amount += (taxable_income - slab) * rate
                    taxable_income = slab

            return tax_amount
        
        income_tax = calculate_income_tax(basic_salary, health_insurance_amount, pension_contribution)

        data = [
            ['Deductions', 'Amount'],
            ['Income Tax', income_tax],
            ['Pension Contribution', pension_contribution],
            ['Health Insurance', health_insurance_amount]
        ]
        table = Table(data, colWidths=[230, 230], hAlign='CENTER')
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),
            ('LINEABOVE', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),
            ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.black) 
        ]))
        payslip_content.append(table)

        gross_salary = basic_salary + housing_allowance + transport_allowance - health_insurance_amount - pension_contribution - income_tax

        payslip_content.append(Paragraph(f'Gross Salary: {gross_salary}', styles['Heading2']))

        italic_center_style = ParagraphStyle(name='Italic', fontName='Helvetica-Oblique', alignment=1, fontSize=10)
        payslip_content.append(Paragraph('For any clarifications, please contact hr@techsture.com', italic_center_style))
        payslip_content.append(Paragraph('Note: This is a System Generated Document and does not require physical signature', italic_center_style))

        doc.build(payslip_content)

        return response

    return render(request, 'payslip.html', {'display_name': display_name, 'position': position, 'profile_pic_url': profile_pic_url, 'menu_list': menu_list, 'months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']})

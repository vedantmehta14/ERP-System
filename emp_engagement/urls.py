from django.contrib import admin
from django.urls import path
from emp_engagement import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('login', views.login_user, name='login_user'),
    path('register',views.register_user, name="register"),

    path("logout",views.logout_user,name="logout_user"),
    path('update_checkout_time/', views.update_checkout_time, name='update_checkout_time'),

    path('index', views.index, name='index'),
    path('home', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('add_announcement/', views.add_announcement, name='add_announcement'),
    path('delete_announcement/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),
    path('user', views.user, name='user'),

    path('adminuser',views.adminuser, name='adminuser'),
    path('get_user_details/<str:username>/', views.get_user_details, name='get_user_details'),
    path('edit_user/', views.edit_user, name='edit_user'),

    path('delete_user/<str:username>', views.delete_user, name='delete_user'),
    path('event', views.event, name='event'),
    path('task', views.task, name='task'),
    path('timesheet', views.timesheet, name='timesheet'),
    path('leave', views.leave, name='leave'),
    path('leave/approve/<str:leave_id>/', views.approve_leave, name='approve_leave'),
    path('leave/reject/<str:leave_id>/', views.reject_leave, name='reject_leave'),
    # path('manageadmin',views.manageadmin, name='Admin Page'),
    # path('activeusers',views.activeusers,name='Active Users'),
    path('policy',views.companypolicy, name='policy'),
    path('checkinout',views.checkinout,name='Check-in Check-out'),
    path('birthdays',views.birthday,name='birthdays'),
    path('payslip',views.payslip,name='payslip'),
    path('holidayspage',views.holidays,name='holidays'),
    path('holidayspage/delete/<str:holiday_id>/', views.delete_holiday, name='delete_holiday'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


AdminMenulist=[
    # ['Home','/home','home'],
    ['Dashboard','/dashboard','grid-alt'],
    ['User','/user','user'],
    ['Event Calendar','/event','calendar'],
    ['Leave','/leave','envelope'],
    ['Payslip','/payslip','rupee'],
    # ['Tasks','/task','task'],
    # ['Check-In Check-Out','/checkinout','check-circle'],
    # ['Birthdays','/birthdays','cake'],
    ['Timesheet','/timesheet','time'],
    ['Holidays','/holidayspage','landscape'],
    ['Company Policy','/policy','buildings'],
    # ['Active Users','/activeusers','user-check'],
    # ['Admin Page','/manageadmin','cog'],
    ['User Management','/adminuser','group'],
    # ['Index','/index']
    
]

UserMenulist=[
    # ['Home','/home','home'],
    ['Dashboard','/dashboard','grid-alt'],
    ['User','/user','user'],
    ['Event Calendar','/event','calendar'],
    ['Leave','/leave','envelope'],
    ['Payslip','/payslip','rupee'],
    # ['Tasks','/task','task'],
    # ['Check-In Check-Out','/checkinout','check-circle'],
    # ['Birthdays','/birthdays','cake'],
    ['Timesheet','/timesheet','time'],
    ['Holidays','/holidayspage','landscape'],
    ['Company Policy','/policy','buildings'],
    # ['Index','/index']
]
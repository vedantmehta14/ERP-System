from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from emp_engagement.models import user_credentials

def login_access_only(view_func):
    def wrapped_view(request,*args, **kwargs):
        try: 
            if 'username' in request.session.keys():
                #print("Hello")
                return view_func(request,*args, **kwargs)
            else:
                #print("Hello2")
                return redirect('/login')
        except:
            #print("Hello1")
            return redirect('/login')
    return wrapped_view

def Admin_only(view_func):
    def wrapped_view(request,*args, **kwargs):
        try:
            if request.session['is_admin'] is True:
                return view_func(request,*args, **kwargs)
            else:
                return redirect('/login')
        except:
            return redirect('/login')
    return wrapped_view
        
def isUser(view_func):
    def wrapped_view(request,*args, **kwargs):
        try:
            if request.session['is_user'] is True:
                return view_func(request,*args, **kwargs)
            else:
                return redirect('/login')
        except:
            print("Hello")
            return redirect('/login')
    return wrapped_view
        
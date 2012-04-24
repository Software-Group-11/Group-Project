from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import django.contrib.auth
from django.template import RequestContext

def login(request):
    redirect_to = request.REQUEST.get('next', '')
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username=username, password=password)
        if user is not None:
            #account exists
            if user.is_active:
                #successful login
                django.contrib.auth.login(request, user)
                return HttpResponseRedirect(redirect_to)
            else:
                #account banned
                return render_to_response('login.html', { 'error': 'Your account has been disabled. Please contact a System Administrator.' }, context_instance=RequestContext(request))
        else:
            #couldn't find user details
            return render_to_response('login.html', { 'error': 'You have entered invalid login credentials. Please check your Username and Password are correct.' }, context_instance=RequestContext(request))
    else:
        #get request
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return render_to_response('login.html', context_instance=RequestContext(request))

def register(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        confirm = request.POST['Confirm_Password']
        email = request.POST['Email']
        if username is None or password is None or confirm is None or email is None:
            return render_to_response('register.html', {'error': 'Please fill in all form fields', 'username':username, 'email':email}, context_instance=RequestContext(request))
        if not password == confirm:
            return render_to_response('register.html', {'error': 'Please ensure both password fields match', 'username':username, 'email': email}, context_instance=RequestContext(request))
        
        try:
            user = User.objects.create_user(username, email)
        except:
            #check that creating a user couldn't throw any other exceptions...
            return render_to_response('site/register.html', {'error': 'This username is already in use'}, context_instance=RequestContext(request))
        user.set_password(password)
        user.save()
        return HttpResponseRedirect('/')
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return render_to_response('register.html', context_instance=RequestContext(request))

def logout(request):
        redirect_to = request.REQUEST.get('next', '')
        django.contrib.auth.logout(request)
        return HttpResponseRedirect(redirect_to)
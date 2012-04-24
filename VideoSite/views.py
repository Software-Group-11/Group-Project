from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import django.contrib.auth
from django.template import RequestContext
from django.db.models import Q
from VideoSite.models import *

def home(request):
    return HttpResponse("Index page saying stuff about the company")
    
def sport(request, sportName):
    sport = get_object_or_404(Sport, name=sportName)
    return render_to_response('site/sport.html', { 'sport': sport }, context_instance=RequestContext(request))

def videosList(request, sportName):
    sport = get_object_or_404(Sport, name=sportName)
    viewModel = {
        'heading': 'Videos for ' + sportName,
        'videos': sport.video_set.all()
    }
    r = RequestContext(request)
    r['sport'] = sport
    return render_to_response('site/list.html', viewModel, context_instance=r)
    
def watchVideo(request, videoId):
    video = get_object_or_404(Video, name=videoId)
    r = RequestContext(request)
    r['sport'] = video.sport
    return render_to_response('site/video.html', {'video': video}, context_instance=r)
    
def postSearch(request):
    if request.method == 'POST':
        searchTerm = request.POST['search']
        return HttpResponseRedirect('/search/' + searchTerm)

def search(request, searchTerm):
    results = Video.objects.filter(Q(name__contains=searchTerm) | Q(description__contains=searchTerm))
    if len(results) is 0:
        viewModel = {
            'heading': 'There are no search results for ' + searchTerm,
            'videos': []
        }
    else:
        viewModel = {
            'heading': 'Search results for ' + searchTerm,
            'videos': results
        }
    return render_to_response('site/list.html', viewModel, context_instance=RequestContext(request))

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
                return render_to_response('site/login.html', { 'error': 'Your account has been disabled. Please contact a System Administrator.' }, context_instance=RequestContext(request))
        else:
            #couldn't find user details
            return render_to_response('site/login.html', { 'error': 'You have entered invalid login credentials. Please check your Username and Password are correct.' }, context_instance=RequestContext(request))
    else:
        #get request
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return render_to_response('site/login.html', context_instance=RequestContext(request))

def register(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        confirm = request.POST['Confirm_Password']
        email = request.POST['Email']
        if username is None or password is None or confirm is None or email is None:
            return render_to_response('site/register.html', {'error': 'Please fill in all form fields', 'username':username, 'email':email}, context_instance=RequestContext(request))
        if not password == confirm:
            return render_to_response('site/register.html', {'error': 'Please ensure both password fields match', 'username':username, 'email': email}, context_instance=RequestContext(request))
        
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
        return render_to_response('site/register.html', context_instance=RequestContext(request))

def logout(request):
        redirect_to = request.REQUEST.get('next', '')
        django.contrib.auth.logout(request)
        return HttpResponseRedirect(redirect_to)
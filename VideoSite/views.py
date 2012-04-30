from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import django.contrib.auth
from datetime import datetime
from django.template import RequestContext
from django.db.models import Q
from VideoSite.models import *

def home(request):
    return render_to_response('about.html', context_instance=RequestContext(request))
    
def sport(request, sportName):
    sport = get_object_or_404(Sport, name=sportName)
    videos = sport.video_set.all()
    latestVideo = []
    nextVideo = []
    today = datetime.now()
    latestVideo = sport.video_set.filter(eventTime__lt=today).order_by('eventTime')[:3]
    nextVideo = sport.video_set.filter(eventTime__gt=today).order_by('eventTime')[:3]
    
    return render_to_response('sport.html', { 'sport': sport, 'latestVideo': latestVideo, 'nextVideo':nextVideo }, context_instance=RequestContext(request))

def videosList(request, sportName):
    sport = get_object_or_404(Sport, name=sportName)
    results = sport.video_set.all()
    if len(results) is 0:
        viewModel = {
            'heading': 'There are no search results for ' + sport.name,
            'videos': []
        }
    else:
        viewModel = {
            'heading': 'Search results for ' + sport.name,
            'videos': results
        }
    r = RequestContext(request)
    r['sport'] = sport
    return render_to_response('list.html', viewModel, context_instance=r)
    
def watchVideo(request, videoId):
    video = get_object_or_404(Video, name=videoId)
    r = RequestContext(request)
    r['sport'] = video.sport
    return render_to_response('video.html', {'video': video}, context_instance=r)
    
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
    return render_to_response('list.html', viewModel, context_instance=RequestContext(request))
 
def addComment(request, videoId):
    #validate incoming data (no blank fields)
    video = get_object_or_404(Video, name=videoId)
    
    if request.POST:
        titlePost = request.POST['Title']
        content = request.POST['Comment']
        if titlePost == "" or content == "":
            return render_to_response('video.html', {'video': video, 'error': 'Please complete both form fields.'}, context_instance=RequestContext(request))
        
        comment = Comment()
        comment.title = titlePost
        comment.content = content
        comment.author = request.user
        comment.video = video
        
        comment.save()
        
        r = RequestContext(request)
        r['sport'] = video.sport
    
    return HttpResponseRedirect('/videos/' + video.name)
    
def changeRating(request, videoId):
    if not request.POST:
        return HttpResponse("Not Accessible by GET")
    
    video = get_object_or_404(Video, name=videoId)
    
    if request.POST['value'] == "+1":
        try:
            video.increaseRating()
            return HttpResponse("Successful")
        except:
            return HttpResponse("Invalid Operation")
    elif request.POST['value'] == "-1":
        try:
            video.decreaseRating()
            return HttpResponse("Successful")
        except Exception as e:
            if e[1] == "Value less than 0":
                #don't show them an error - this will happen far too often
                return HttpResponse("Successful")
            else:
                return HttpResponse("Invalid Operation")
            
    else:
        return HttpResponse("Invalid Request")

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
    videos = sport.video_set.all()
    latestVideo = []
    nextVideo = []
    for video in videos:
      if hasOccurred(video):
        latestVideo.append(video)
      else:
        nextVideo.append(video)
        
    latestVideo = max
    
    
    
    return render_to_response('sport.html', { 'sport': sport, 'latestVideo': latestVideo, 'nextVideo':nextVideo }, context_instance=RequestContext(request))

def videosList(request, sportName):
    sport = get_object_or_404(Sport, name=sportName)
    viewModel = {
        'heading': 'Videos for ' + sportName,
        'videos': sport.video_set.all()
    }
    r = RequestContext(request)
    r['sport'] = sport
    return render_to_response('list.html', viewModel, context_instance=r)
    
def watchVideo(request, videoId):
    print "test"
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

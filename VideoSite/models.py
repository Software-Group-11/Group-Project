from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Sport(models.Model):
    name = models.CharField(max_length=200)
    
    def getVideos(self):
        #return a list of videos for this sport
        pass
    
    def __unicode__(self):
        return self.name

class Video(models.Model):
        name = models.CharField(max_length=200)
        description = models.TextField()
        sport = models.ForeignKey(Sport)
        pictureLocation = models.CharField("Youtube ID", max_length=200)
        rating = models.IntegerField()
        eventTime = models.DateTimeField("Event Time", auto_now=False)
        uploadTime = models.DateTimeField("Date Uploaded", auto_now=True)
        
        def toHtml(self):
            #return a html representation of a video.
            pass
            
        def increaseRating(self):
            #increase the rating of the video by 1
            pass
        
        def decreaseRating(self):
            #decrease the rating of the video by 1
            pass
            
        def hasOccurred(self):
            #uses the date of the event to determine if it is in the future, 
            #or has already happened
            #return a bool (True for has happened, False for in the future)
            pass
        
        def __unicode__(self):
            #used by django for labels and stuff
            return self.name
        
            

class Comment(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User)
    uploadTime = models.DateTimeField("Date Uploaded", auto_now=True)
    video = models.ForeignKey(Video)
    
    def toHtml(self):
        #return a html representation of a comment
        pass
        
    def __unicode__(self):
        return self.title

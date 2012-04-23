from VideoSite.models import Video, Comment, Sport
from django.contrib import admin

class CommentInline(admin.StackedInline):
    model = Comment
    extras = 0
    
class VideoAdmin(admin.ModelAdmin):
    fieldsets = [
    (None, {'fields': ['name', 'eventTime', 'description', 'sport', 'pictureLocation', 'rating']}),
    ]
    inlines = [CommentInline]
    list_filter = ('uploadTime', 'eventTime')
    search_fields = ['name']


admin.site.register(Video, VideoAdmin)
admin.site.register(Sport)

from django.db import models
from django.contrib.comments.models import Comment

class CommentWithRatings(Comment):
    title = models.CharField(max_length=255)
    rating = models.IntegerField(null=True, blank=True)
    age = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    

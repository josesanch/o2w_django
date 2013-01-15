from django.contrib import admin
from models import CommentWithRatings
from django.contrib.comments.admin import CommentsAdmin


admin.site.register(CommentWithRatings, CommentsAdmin)

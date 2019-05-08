from django.contrib import admin

from .models import Post, Comment, Reply, CommentVote, Vote, Saved
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(CommentVote)
admin.site.register(Vote)
admin.site.register(Saved)
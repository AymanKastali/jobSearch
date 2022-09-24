from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(PostComment)
admin.site.register(PostCommentLike)
admin.site.register(PostCommentReply)
admin.site.register(PostCommentReplyLike)
admin.site.register(JobPost)
admin.site.register(JobPostCandidate)
admin.site.register(Tag)
admin.site.register(SavedPost)
admin.site.register(SavedJobPost)
admin.site.register(ChatMessage)
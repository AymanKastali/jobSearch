from django.db import models
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    work_title = models.CharField(max_length=200, blank=True, null=True)
    about = models.CharField(max_length=200, blank=True, null=True)
    pic = models.ImageField(default="profile-pic.png", null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    
    profile_experience = models.CharField(max_length=2000, blank=True, null=True)
    profile_language = models.CharField(max_length=75, blank=True, null=True)
    profile_education = models.CharField(max_length=50, blank=True, null=True)
    profile_resume = models.FileField(upload_to='media/', blank=True, null=True)
    profile_skills = models.CharField(max_length=2000, blank=True, null=True)

    page_employee_num = models.CharField(max_length=2000, blank=True, null=True)
    page_location = models.CharField(max_length=2000, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    is_page = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name or ''
    
    @property
    def get_date(self):
        return humanize.naturaltime(self.created_at)

    
class Post(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    post_text = models.CharField(max_length=200, blank=True, null=True)
    post_pic = models.ImageField(null=True, blank=True)
    post_video = models.FileField(upload_to='media/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return str(self.post_text)

    @property
    def get_date(self):
        return humanize.naturaltime(self.created_at)
    
    @property
    def post_comments(self):
        comments = self.postcomment_set.all()
        return comments
    
    @property
    def post_likes(self):
        post_likes = self.postlike_set.filter(like=True)
        return post_likes
    
    @property
    def comments_count(self):
        comments = self.postcomment_set.all().count()
        return comments
    @property
    def likes_count(self):
        likes = self.postlike_set.filter(like=True).count()
        return likes
    
    @property
    def is_liked(self):
        value = self.postlike_set.filter(like=True)
        return value
    
    @property
    def get_post_likes_arr(self):
        value = self.postlike_set.all()
        users_liked_arr = [ i.user for i in value ]
        return users_liked_arr
    
class PostLike(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.like)
    
class PostComment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return str(self.comment)
    
    
    @property
    def get_date(self):
        return humanize.naturaltime(self.created_at)
    
    @property
    def comment_likes_count(self):
        likes = self.postcommentlike_set.filter(like=True).count()
        return likes
    
    @property
    def comment_replies(self):
        replies = self.postcommentreply_set.all()
        return replies

    @property
    def comment_replies_count(self):
        replies = self.postcommentreply_set.all().count()
        return replies

    @property
    def is_liked(self):
        value = self.postcommentlike_set.filter(like=True)
        return value
    
    @property
    def get_post_comment_likes_arr(self):
        value = self.postcommentlike_set.all()
        users_liked_arr = [ i.user for i in value ]
        return users_liked_arr
    
class PostCommentLike(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(PostComment, null=True, blank=True, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.like)
    
class PostCommentReply(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(PostComment, null=True, blank=True, on_delete=models.CASCADE)
    reply = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.reply
    
    @property
    def get_date(self):
        return humanize.naturaltime(self.created_at)
    
    @property
    def replie_likes_count(self):
        likes = self.postcommentreplylike_set.filter(like=True).count()
        return likes
    
    @property
    def is_liked(self):
        value = self.postcommentreplylike_set.filter(like=True)
        return value
    
    @property
    def get_post_likes_arr(self):
        value = self.postcommentreplylike_set.all()
        users_liked_arr = [ i.user for i in value ]
        return users_liked_arr
    
    
class PostCommentReplyLike(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    reply = models.ForeignKey(PostCommentReply, null=True, blank=True, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return str(self.like)
    
    
class JobPost(models.Model):
    CHOISES = (
        ('Part Time', 'Part Time'),
        ('Full Time', 'Full Time'),
    )
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200, blank=True, null=True)
    responsabilities = models.CharField(max_length=500, blank=True, null=True)
    experiense = models.CharField(max_length=700, blank=True, null=True)
    required_skills = models.CharField(max_length=200, blank=True, null=True)
    job_time = models.CharField(max_length=9, blank=True, null=True, choices=CHOISES)
    city = models.CharField(max_length=20, blank=True, null=True)
    salary = models.CharField(max_length=100, blank=True, null=True)
    state = models.BooleanField(default=True)
    tag = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.job_title
    
    @property
    def get_date(self):
        return humanize.naturaltime(self.created_at)
    
    @property
    def get_candidates(self):
        candidates = self.jobpostcandidate_set.all()
        return candidates
    
    @property
    def get_candidates_count(self):
        num = self.jobpostcandidate_set.all().count()
        return num

    @property
    def get_nominees(self):
        candidates = self.jobpostcandidate_set.filter(state=True)
        return candidates
    
    @property
    def get_nominees_count(self):
        candidates = self.jobpostcandidate_set.filter(state=True).count()
        return candidates
    
    @property
    def get_accepted_nominee(self):
        nominee = self.jobpostcandidate_set.get(accepted=True)
        return nominee
    
class JobPostCandidate(models.Model):
    job_post = models.ManyToManyField(JobPost)
    user = models.ManyToManyField(User)
    state = models.BooleanField(default=False)
    hired = models.BooleanField(default=False)
    
    interview_date = models.CharField(max_length=20, blank=True, null=True)
    interview_time = models.CharField(max_length=20, blank=True, null=True)
    
    notes = models.CharField(max_length=2048, blank=True, null=True)
    accepted = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True) 
    
    def __str__(self):
        return str(self.state)
    
    
class Tag(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    tag = models.CharField(max_length=25, blank=True, null=True)
    
    def __str__(self):
        return self.tag
    

class SavedPost(models.Model):
    user = models.ManyToManyField(User)
    post = models.ManyToManyField(Post)
    
    def __str__(self):
        return f'{self.user} + {self.post}'
    
    
class SavedJobPost(models.Model):
    user = models.ManyToManyField(User)
    jobpost = models.ManyToManyField(JobPost)
        
    def __str__(self):
        return f'{self.user} + {self.jobpost}'
    
class ChatMessage(models.Model):
    from_user = models.ForeignKey(User,related_name='messages', null=True, blank=True, on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,related_name='to_user_messages', null=True, blank=True, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message
    
    @property
    def get_date(self):
        return humanize.naturaltime(self.created_at)
    
    class Meta:
        ordering = ('created_at',)
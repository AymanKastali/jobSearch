from django import forms
from .models import *
        
class DatePickerInput(forms.DateInput):
    input_type = 'date'
    
class TimePickerInput(forms.TimeInput):
        input_type = 'time'

class ProfileForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=DatePickerInput(attrs={'class':'form-control datetimepicker-input'}))
    work_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    about = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    pic = forms.FileField(widget=forms.FileInput(attrs={'class':"form-control" ,'id':"inputGroupFile02"}))
    profile_experience = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    profile_language = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_education = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_skills = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    profile_resume = forms.FileField(widget=forms.FileInput(attrs={'class':"form-control" ,'id':"inputGroupFile02"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) 

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user','is_page','page_employee_num','page_location']
        
class PageForm(forms.ModelForm)  :
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=DatePickerInput(attrs={'class':'form-control datetimepicker-input'}))
    work_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    about = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    pic = forms.FileField(widget=forms.FileInput(attrs={'class':"form-control" ,'id':"inputGroupFile02"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    page_employee_num = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    page_location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user','is_page', 'profile_experience', 'profile_language', 'profile_education', 'profile_skills', 'profile_resume']
        
        
class PostForm(forms.ModelForm):
    post_text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Start a post..'}))
    post_pic = forms.FileField(required=False, widget=forms.FileInput(attrs={'class':"form-control" ,'id':"inputGroupFile02"}))
    post_video = forms.FileField(required=False, widget=forms.FileInput(attrs={'class':"form-control" ,'id':"inputGroupFile02"}))
    class Meta:
        model = Post
        fields = ['post_pic', 'post_video', 'post_text']
        
class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    class Meta:
        model = PostComment
        fields = ['comment']
        
class PostCommentReplyForm(forms.ModelForm):
    reply = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reply..'}))
    class Meta:
        model = PostCommentReply
        fields = ['reply']
        
class JobPostForm(forms.ModelForm):
    CHOISES = (
        ('Part Time', 'Part Time'),
        ('Full Time', 'Full Time'),
    )
    job_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    responsabilities = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '8'}))
    experiense = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '8'}))
    required_skills = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}))
    job_time = forms.CharField(widget=forms.Select(choices=CHOISES, attrs={'class': "form-select"}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    salary = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = JobPost
        fields = '__all__'
        exclude = ['user', 'state']

class TagForm(forms.ModelForm):
    tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add a job Tag..'}))
    class Meta:
        model = Tag
        fields = ['tag']
        
class AppointmentForm(forms.ModelForm):
    interview_date = forms.CharField(widget=DatePickerInput(attrs={'class':'form-control datetimepicker-input'}))
    interview_time = forms.CharField(widget=TimePickerInput(attrs={'class':'form-control datetimepicker-input'}))
    class Meta:
        model = JobPostCandidate
        fields = ['interview_date', 'interview_time']
    
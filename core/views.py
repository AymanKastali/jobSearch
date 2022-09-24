from colorsys import rgb_to_yiq
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from friendship.models import Friend, Follow, Block, FriendshipRequest
from .filters import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

@login_required(login_url='account_login')
def home(request):
    post_form = PostForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_form.instance.user = request.user
            post_form.save()
            return redirect('home')
    user_posts_arr = [post for post in Post.objects.filter(user=request.user)]
    pages_following_posts_arr = []
    posts = Post.objects.all()
    followings = Follow.objects.following(request.user)
    followings_count = len(followings)
    
    followers = Follow.objects.followers(request.user)
    followers_count = len(followers)
    
    for post in posts:
        for following in followings:
            if following.id == post.user.id:
                pages_following_posts_arr.append(post)  
    firends_posts_arr = [post for post in posts if Friend.objects.are_friends(request.user, post.user) ]
    user_posts = user_posts_arr + firends_posts_arr + pages_following_posts_arr 
    jobPosts = JobPost.objects.all()
    post_form = PostForm()

    posts_count = request.user.post_set.all().count()
    friend_requests = FriendshipRequest.objects.filter(to_user=request.user.id)
    connections_count = len(Friend.objects.friends(request.user))
    requests_counts = len(friend_requests)
    blocked_people = Block.objects.blocking(request.user)
    blocked_people_count = len(blocked_people)
    comment_add_form = CommentForm()
    comment_reply_form = PostCommentReplyForm()

    followers_count = len(Follow.objects.followers(request.user))
    following_posts_arr = []
    for post in posts:
        for following in Follow.objects.following(request.user):
            if following.id == post.user.id:
                following_posts_arr.append(post)  
    page_posts_arr = [ post for post in Post.objects.filter(user=request.user) ]
    page_home_posts =  page_posts_arr + following_posts_arr
    
    tag_form = TagForm()
    user_tags = Tag.objects.filter(user=request.user)
    
    saved_posts_count = Post.objects.filter(savedpost__user=request.user).count()
    saved_jobposts_count = JobPost.objects.filter(savedjobpost__user=request.user).count()

    saved_posts = Post.objects.filter(savedpost__user=request.user)
    saved_jobposts = JobPost.objects.filter(savedjobpost__user=request.user)

    user_jobposts = JobPost.objects.filter(user=request.user)
    user_jobposts_arr = [ i for i in user_jobposts ]
    user_jobposts_count = len(user_jobposts_arr)
    
    chats = ChatMessage.objects.filter(from_user = request.user)
    chats_to_users_arr = [ chat.to_user for chat in chats ]
    print(set(chats_to_users_arr))
    
    last_message_arr = []
    for user in set(chats_to_users_arr):
        to_user_chats = ChatMessage.objects.filter(from_user=request.user, to_user=user.id)
        to_user_chats_arr = list(to_user_chats)
        last_msg = to_user_chats_arr[len(to_user_chats_arr)-1]
        last_message_arr.append(last_msg)
    print('last arr:', last_message_arr)
    # chats = ChatMessage.objects.filter(from_user=request.user).order_by().values('to_user').distinct()
    
    context = {
        'user_posts': user_posts,
        'posts': posts,
        'post_form': post_form,
        'jobPosts': jobPosts,
        'posts_count': posts_count,
        'friend_requests': friend_requests,
        'connections_count': connections_count,
        'requests_counts': requests_counts,
        'blocked_people_count': blocked_people_count,
        'comment_add_form': comment_add_form,
        'comment_reply_form': comment_reply_form,
        'followers_count': followers_count,
        'page_home_posts': page_home_posts,
        'tag_form': tag_form,
        'user_tags': user_tags,
        'saved_posts_count': saved_posts_count,
        'saved_jobposts_count': saved_jobposts_count,
        'saved_posts': saved_posts,
        'saved_jobposts': saved_jobposts,
        'followings_count': followings_count,
        'user_jobposts_count': user_jobposts_count,
        'last_message_arr': last_message_arr,
    }
    return render(request, 'core/home.html', context)

@login_required(login_url='account_login')
def save_post(request, postId):
    user = request.user
    post = Post.objects.get(id=postId)
    if request.method == "POST":
        saved_post = SavedPost.objects.create()
        saved_post.user.add(user)
        saved_post.post.add(post)
    return redirect('home')

@login_required(login_url='account_login')
def saved_posts(request):
    saved_posts = Post.objects.filter(savedpost__user=request.user)
    context = {
        'saved_posts': saved_posts,
    }
    return render(request, 'core/saved_posts.html', context)

@login_required(login_url='account_login')
def save_jobpost(request, postId):
    user = request.user
    jobpost = JobPost.objects.get(id=postId)
    if request.method == "POST":
        saved_jobpost = SavedJobPost.objects.create()
        saved_jobpost.user.add(user)
        saved_jobpost.jobpost.add(jobpost)
    return redirect('home')

@login_required(login_url='account_login')
def saved_jobposts(request):
    saved_jobposts = JobPost.objects.filter(savedjobpost__user=request.user)
    context = {
        'saved_jobposts': saved_jobposts,
    }
    return render(request, 'core/saved_jobposts.html', context)

@login_required(login_url='account_login')
def tag_add(request):
    tag_form = TagForm()
    if request.method == 'POST':
        tag_form = TagForm(request.POST)
        if tag_form.is_valid():
            tag_form.instance.user = request.user
            tag_form.save()
            return redirect('home')

@login_required(login_url='account_login')
def create_profile_or_page(request):
    group = Group.objects.get(name=request.POST.get('group'))
    if request.method == 'POST':  
        profile = Profile.objects.create(user=request.user)
        if request.POST.get('group') == 'profile':
            request.user.groups.add(group)
        elif request.POST.get('group') == 'page':
            request.user.groups.add(group)
            profile.is_page = True
        profile.save()
        
    return redirect('profile')

@login_required(login_url='account_login')
def profile(request):
    groups = Group.objects.all()
    pages = Profile.objects.filter(is_page=True)
    job_posts = JobPost.objects.filter(user=request.user)[:3]
    Profile_form = ProfileForm()
    groups = Group.objects.all()
    suggestions = Profile.objects.all()
    is_following = Follow.objects.following(request.user)
    
    if Profile.objects.filter(user=request.user).exists():
        profile = Profile.objects.get(user=request.user.id)
        if request.user.profile.is_page == False:
            not_friends_arr = [suggestion for suggestion in suggestions if Friend.objects.are_friends(request.user, suggestion.user) == False ]
        else:
            not_friends_arr = []
        connections_request_from_users_id_arr = [con.from_user.id for con in Friend.objects.unread_requests(user=request.user)]
        connections_request_sent_id_arr = [con.to_user.id for con in Friend.objects.sent_requests(user=request.user)]
        page_posts = Post.objects.filter(user=request.user)[:2]
    else:
      profile = ''
      not_friends_arr = []
      connections_request_from_users_id_arr = []
      connections_request_sent_id_arr= []
      page_posts = ''
      print(request.user)
    context = {
        'groups': groups,
        'Profile_form': Profile_form,
        'profile': profile,
        'pages': pages,
        'suggestions': suggestions,
        'is_following': is_following,
        'not_friends_arr': not_friends_arr,
        'connections_request_from_users_id_arr': connections_request_from_users_id_arr,
        'connections_request_sent_id_arr': connections_request_sent_id_arr,
        'job_posts': job_posts,
        'page_posts': page_posts,
    }
    return render(request, 'core/profile.html', context)

@login_required(login_url='account_login')
def profile_edit(request):
    profile = request.user.profile
    profile_form = ProfileForm(instance=profile)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            print(request.POST)
            profile_form.instance.user = request.user
            profile_form.save()
            return redirect('profile')
    context = {
        'profile_form': profile_form,
               }
    return render(request, 'core/user_profile_edit.html', context)
   
@login_required(login_url='account_login')         
def page_edit(request):
    profile = request.user.profile
    page_form = PageForm(instance=profile)
    if request.method == 'POST':
        page_form = PageForm(request.POST, request.FILES, instance=profile)
        if page_form.is_valid():
            print(request.POST)
            page_form.instance.user = request.user
            page_form.save()
            return redirect('profile')
    context = {
        'page_form': page_form,
               }
    return render(request, 'core/user_page_edit.html', context)

@login_required(login_url='account_login')   
def connections(request):
    connections = Friend.objects.friends(request.user)
    context = {
        'connections': connections,
    }
    return render(request, 'core/connections.html', context)

@login_required(login_url='account_login')
def followings(request):
    followings = Follow.objects.following(request.user)
    context = {
        'followings': followings,
    }
    return render(request, 'core/followings.html', context)

@login_required(login_url='account_login')
def followers(request):
    followers = Follow.objects.followers(request.user)
    context = {
        'followers': followers,
    }
    return render(request, 'core/followers.html', context)

@login_required(login_url='account_login')
def blocks(request):
    blocks = Block.objects.blocking(request.user)
    context = {
        'blocks': blocks,
    }
    return render(request, 'core/blocks.html', context)

@login_required(login_url='account_login')
def requests(request):
    requests = FriendshipRequest.objects.filter(to_user=request.user)
    requests_from_users_arr = [request.from_user for request in requests]
    context = {
        'requests_from_users_arr': requests_from_users_arr,
    }
    return render(request, 'core/requests.html', context)

@login_required(login_url='account_login')
def connection_request_accept(request):
    from_user = request.POST.get('userId')
    friend_request = FriendshipRequest.objects.get(from_user= from_user, to_user=request.user)
    friend_request.accept()
    return redirect('home')  

@login_required(login_url='account_login')
def connection_request_reject(request):
    from_user = request.POST.get('userId')
    friend_request = FriendshipRequest.objects.get(from_user= from_user, to_user=request.user)
    friend_request.reject()
    return redirect('home')

@login_required(login_url='account_login')
def connection_request_decline(request):
    from_user = request.POST.get('userId')
    friend_request = FriendshipRequest.objects.get(from_user= from_user, to_user=request.user)
    friend_request.reject()
    return redirect('home')

@login_required(login_url='account_login')
def connection_add(request):
    if request.method == 'POST':
        to_user = User.objects.get(id=request.POST.get('userId'))
        Friend.objects.add_friend(
            request.user,
            to_user)
    return redirect('profile')

@login_required(login_url='account_login')
def connection_remove(request, userId):
    other_user = User.objects.get(id=userId)
    if request.method == "POST":
        Friend.objects.remove_friend(request.user, other_user)
        return redirect('profile-connections')
    context = {
        'other_user': other_user
    }
    return render(request, 'core/connection_remove.html', context)

@login_required(login_url='account_login')
def connection_block(request, userId):
    other_user = User.objects.get(id=userId)
    if request.method == "POST":
        Block.objects.add_block(request.user, other_user)
        return redirect('profile-connections')
    context = {
        'other_user': other_user
    }

    return render(request, 'core/connection_block.html', context)    

@login_required(login_url='account_login')
def connection_profile(request, userId):
    user = User.objects.get(id=userId)
    is_connected = Friend.objects.friends(request.user)
    employee = user.employee
    context = {
        'employee': employee,
        'is_connected': is_connected,
    }
    return render(request, 'core/connection_profile.html', context)

@login_required(login_url='account_login')
def user_profile(request, userId):
    user = User.objects.get(id=userId)
    profile = Profile.objects.get(user=user)
    is_connected = Friend.objects.friends(request.user)
    is_friends = Friend.objects.are_friends(request.user, profile.user) 
    suggestions = Profile.objects.all()
    
    is_following = Follow.objects.following(request.user)
    not_friends_arr = [suggestion for suggestion in suggestions if Friend.objects.are_friends(request.user, suggestion.user) == False ]
    connections_request_from_users_id_arr = [con.from_user.id for con in Friend.objects.unread_requests(user=request.user)]
    connections_request_sent_id_arr = [con.to_user.id for con in Friend.objects.sent_requests(user=request.user)]
    
    context = {
        'is_friends': is_friends,
        'profile': profile,
        'is_connected': is_connected,
        'suggestions': suggestions,
        'is_following': is_following,
        'not_friends_arr': not_friends_arr,
        'connections_request_from_users_id_arr' : connections_request_from_users_id_arr,
        'connections_request_sent_id_arr': connections_request_sent_id_arr,
    }
    return render(request, 'core/user_profile.html', context)

@login_required(login_url='account_login')
def user_page(request, userId):
    user = User.objects.get(id=userId)
    page = Profile.objects.get(user=user)
    profiles = Profile.objects.filter(is_page=False)
    is_following = Follow.objects.following(request.user)    
    is_following_arr = [i.id for i in is_following]
    posts = Post.objects.filter(user=user)[:2]
    job_posts = JobPost.objects.filter(user=user)
    
    pages = Profile.objects.filter(is_page=True)

    not_friends_arr = [profile for profile in profiles if Friend.objects.are_friends(request.user, profile.user) == False ]
    connections_request_from_users_id_arr = [con.from_user.id for con in Friend.objects.unread_requests(user=request.user)]
    connections_request_sent_id_arr = [con.to_user.id for con in Friend.objects.sent_requests(user=request.user)]

    context = {
        'page': page,
        'profiles': profiles,
        'pages': pages,
        'is_following': is_following,
        'is_following_arr': is_following_arr,
        'posts': posts,
        'user': user,
        'job_posts': job_posts,
        'not_friends_arr': not_friends_arr,
        'connections_request_from_users_id_arr': connections_request_from_users_id_arr,
        'connections_request_sent_id_arr': connections_request_sent_id_arr,
    }
    return render(request, 'core/user_page.html', context)

@login_required(login_url='account_login')
def user_page_posts(request, userId):
    user = User.objects.get(id=userId)
    posts = Post.objects.filter(user=user)
    context = {
        'posts': posts,
    }
    return render(request, 'core/user_page_posts.html', context)

@login_required(login_url='account_login')
def user_page_jobposts(request, userId):
    user = User.objects.get(id=userId)
    jobposts = JobPost.objects.filter(user=user)
    context = {
        'jobposts': jobposts,
    }
    return render(request, 'core/user_page_jobposts.html', context)

@login_required(login_url='account_login')
def jobpost_view(request, userId, jobId):
    user = User.objects.get(id=userId)
    post = JobPost.objects.get(id=jobId)
    candidate = request.user.jobpostcandidate_set.filter(job_post=post)
    if candidate.exists():
        candidate = candidate[0]
    else:
        candidate
    candidates_arr = [ candidate for candidate in post.get_candidates ]
    
    saved_jobposts = JobPost.objects.filter(savedjobpost__user=request.user)
    context = {
        'post': post,
        'candidate': candidate,
        'candidates_arr': candidates_arr,
        'saved_jobposts': saved_jobposts,
    }
    return render(request, 'core/user_page_jobpost.html', context)

@login_required(login_url='account_login')
def jobs_applied(request):
    jobs_applied = JobPost.objects.filter(jobpostcandidate__user=request.user)
    context = {
        'jobs_applied': jobs_applied,
    }
    return render(request, 'core/jobs_applied.html', context)

@login_required(login_url='account_login')
def jobposts(request):
    job_posts = JobPost.objects.all()
    job_posts_filter = JobPostFilter(request.GET, queryset=job_posts)
    job_posts = job_posts_filter.qs
    p = Paginator(job_posts, 10)
    page_num = request.GET.get('page', 1)
    try:
        job_posts = p.page(page_num)
    except EmptyPage:
        job_posts = p.page(1)
    except PageNotAnInteger:
        job_posts = p.page(1)
    context = {
        'job_posts': job_posts,
        'job_posts_filter': job_posts_filter,
    }
    return render(request, 'core/jobposts.html', context)

@login_required(login_url='account_login')
def job_apply(request, userId, jobId):    
    user = request.user
    job_post = JobPost.objects.get(id=jobId)
    candidate = JobPostCandidate.objects.create()
    candidate.user.add(user)
    candidate.job_post.add(job_post)
    
    return redirect('profile-jobposts')

@login_required(login_url='account_login')
def profile_follow(request):
    other_user = User.objects.get(id=request.POST.get('userId'))
    if request.method == 'POST':
        Follow.objects.add_follower(request.user, other_user)
        return redirect('profile')

@login_required(login_url='account_login')
def profile_unfollow(request):
    other_user = User.objects.get(id=request.POST.get('userId'))
    if request.method == 'POST':
        Follow.objects.remove_follower(request.user, other_user)
        return redirect('profile')
 
@login_required(login_url='account_login')   
def posts(request):
    profile = Profile.objects.filter(user=request.user)
    posts = Post.objects.filter(user=request.user)
    context = {
        'posts': posts,
        'profile': profile,
    }
    return render(request, 'core/posts.html', context)

@login_required(login_url='account_login')
def post_edit(request, postId):
    post = Post.objects.get(id=postId)
    post_form = PostForm(instance=post)
    if request.method == 'POST':
        if post.user.id == request.user.id:
            post_form = PostForm(request.POST, request.FILES, instance=post)
            post_form.save()
            return redirect('profile-posts')
    context = {
        'post_form': post_form
    }
    return render(request, 'core/post_edit.html', context)

@login_required(login_url='account_login')
def post_delete(request, postId):
    post = Post.objects.get(id=postId)
    if request.method == 'POST':
        post.delete()
        return redirect('profile-posts')
    context = {
        'post': post
    }
    return render(request, 'core/post_delete.html', context)  

@login_required(login_url='account_login')
def post_like(request, postId):
    post = Post.objects.get(id=postId)
    post_like = PostLike.objects.create(post=post)
    post_like = PostLike.objects.get(id=post_like.id)
    post_like.user = request.user
    post_like.like = True  
    post_like.save()
    # return HttpResponse(status=204)
    return redirect('home')

@login_required(login_url='account_login')
def post_unlike(request, postId):
    post = Post.objects.get(id=postId)
    post_unlike = PostLike.objects.get(post=post)
    # post_dislike.like = False  
    post_unlike.delete()
    # return HttpResponse(status=204)
    return redirect('home')

@login_required(login_url='account_login')
def post_comment(request, postId):
    post = Post.objects.get(id=postId)
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.user = request.user
            comment_form.instance.post = post
            comment_form.save()
    return redirect('home')

@login_required(login_url='account_login')
def post_comment_edit(request,postId, commentId):
    comment = PostComment.objects.get(id=commentId)
    comment_form = CommentForm(instance=comment)
    if request.method == 'POST':
        if comment.user.id == request.user.id:
            comment_form = CommentForm(request.POST, instance=comment)
            if comment_form.is_valid():
                comment_form.save()
                return redirect('home')
    context = {
        'comment_form': comment_form,
    }
    return render(request, 'core/comment_edit.html', context)

@login_required(login_url='account_login')
def post_comment_delete(request, postId, commentId):
    comment = PostComment.objects.get(id=commentId)
    if request.method == 'POST':
        if comment.user.id == request.user.id:
            comment.delete()
            return redirect('home')
    context = {
        'comment': comment,
    }
    return render(request, 'core/comment_delete.html', context)

@login_required(login_url='account_login')
def post_comment_reply(request, postId, commentId):
    post = Post.objects.get(id=postId)
    comment = PostComment.objects.get(id=commentId)
    reply_form = PostCommentReplyForm()
    if request.method == 'POST':
        reply_form = PostCommentReplyForm(request.POST)
        if reply_form.is_valid():
            reply_form.instance.comment = comment
            reply_form.instance.user = request.user
            reply_form.save()
            return redirect('home')

@login_required(login_url='account_login')      
def post_comment_reply_edit(request, postId, commentId, replyId):
    reply = PostCommentReply.objects.get(id=replyId)
    reply_form = PostCommentReplyForm(instance=reply)
    if request.method == 'POST':
        if reply.user.id == request.user.id:
            reply_form = PostCommentReplyForm(request.POST, instance=reply)
            if reply_form.is_valid():
                reply_form.save()
                return redirect('home')
    context = {
        'reply_form': reply_form,
    }
    return render(request, 'core/reply_edit.html', context)

@login_required(login_url='account_login')
def post_comment_reply_delete(request, postId, commentId, replyId):
    reply = PostCommentReply.objects.get(id=replyId)
    if request.method == 'POST':
        if reply.user.id == request.user.id:
            reply.delete()
            return redirect('home')
    context = {
        'reply': reply,
    }
    return render(request, 'core/reply_delete.html', context)    

@login_required(login_url='account_login')
def post_comment_like(request, postId, commentId):
    comment = PostComment.objects.get(id=commentId)
    if request.method == 'POST':
        post_comment_like = PostCommentLike.objects.create(comment=comment)
        post_comment_like.user = request.user
        post_comment_like.like = True
        post_comment_like.save()
        # return HttpResponse(status=204)
        return redirect('home')

@login_required(login_url='account_login')  
def post_comment_unlike(request, postId, commentId):
    comment = PostComment.objects.get(id=commentId)
    if request.method == 'POST':
        post_comment_like = PostCommentLike.objects.get(comment=comment)
        post_comment_like.delete()
        # return HttpResponse(status=204)
        return redirect('home')

@login_required(login_url='account_login')    
def post_comment_likes_page(request, postId, commentId):
    comment = PostComment.objects.get(id=commentId)
    context = {
        'comment': comment,
    }
    return render(request, 'core/comment_likes.html', context)

@login_required(login_url='account_login')
def post_comment_reply_likes_page(request, postId, commentId, replyId):
    reply = PostCommentReply.objects.get(id=replyId)
    context = {
        'reply': reply,
    }
    return render(request, 'core/reply_likes_page.html', context)

@login_required(login_url='account_login')     
def post_comment_reply_like(request, postId, commentId, replyId):
    reply = PostCommentReply.objects.get(id=replyId)
    if request.method == 'POST':
        post_comment_reply_like = PostCommentReplyLike.objects.create(reply=reply)
        post_comment_reply_like.user = request.user
        post_comment_reply_like.like = True
        post_comment_reply_like.save()
        # return HttpResponse(status=204)
        return redirect('home')

@login_required(login_url='account_login')       
def post_comment_reply_unlike(request, postId, commentId, replyId):
    reply = PostCommentReply.objects.get(id=replyId)
    if request.method == 'POST':
        post_comment_reply_like = PostCommentReplyLike.objects.get(reply=reply)
        post_comment_reply_like.delete()
        # return HttpResponse(status=204)
        return redirect('home')

@login_required(login_url='account_login')     
def follower_profile(request, userId):
    user = User.objects.get(id=userId)
    is_follower_arr = Follow.objects.followers(request.user)
    print(is_follower_arr)
    context = {}
    return render(request, 'core', context)

@login_required(login_url='account_login') 
def follower_block(request, userId):
    user = User.objects.get(id=userId)
    if request.method == "POST":
        Block.objects.add_block(request.user, user)
        return redirect('home')
    context = {
        'user': user,
    }
    return render(request, 'core/follower_block.html', context)

@login_required(login_url='account_login')
def followers(request):
    followers = Follow.objects.followers(request.user)
    print(followers)
    context = {
        'followers': followers,
    }
    return render(request, 'core/followers.html', context)

@login_required(login_url='account_login')
def user_jobposts(request):
    job_posts = JobPost.objects.all()
    job_posts_filter = JobPostFilter(request.GET, queryset=job_posts)
    job_posts = job_posts_filter.qs
    p = Paginator(job_posts, 6)
    page_num = request.GET.get('page', 1)
    try:
        job_posts = p.page(page_num)
    except EmptyPage:
        job_posts = p.page(1)
    except PageNotAnInteger:
        job_posts = p.page(1)
    context = {
        'job_posts': job_posts,
        'job_posts_filter': job_posts_filter,
        }
    return render(request, 'core/user_jobposts.html', context)

@login_required(login_url='account_login')
def tag_jobposts(request):
    tag = request.POST.get('tag')
    jobPosts = JobPost.objects.all()
    tags_arr = [ tag_item.tag for tag_item in jobPosts ]
    # tags_arr = list(chain.from_iterable(tags_arr))
    tag_arr = []
    for tag_item in tags_arr:
        if tag in tag_item:
            tag_arr.append(tag_item)
    tag_posts = JobPost.objects.filter(tag__in=tag_arr)
    context = {
        'tag_posts': tag_posts,
    }
    return render(request, 'core/tag_jobposts.html', context)

@login_required(login_url='account_login')
def tag_jobposts_delete(request):
    tagId = request.POST.get('tagId')
    tag = Tag.objects.get(id=tagId)
    if request.method == 'POST':
        tag.delete()
        return redirect('home')

@login_required(login_url='account_login')  
def profile_jobposts(request):
    jobposts = JobPost.objects.filter(user=request.user)
    context = {
        'jobposts': jobposts,
    }
    return render(request, 'core/profile_jobposts.html', context)

@login_required(login_url='account_login')
def profile_jobpost_add(request):
    jobpost_form = JobPostForm()
    if request.method == 'POST':
        jobpost_form = JobPostForm(request.POST)
        if jobpost_form.is_valid():
            jobpost_form.instance.user = request.user
            jobpost_form.save()
            return redirect('profile')
    context = {
        'jobpost_form': jobpost_form,
    }
    return render(request, 'core/jobpost_add.html', context)

@login_required(login_url='account_login')
def profile_jobpost_view(request, postId):
    jobpost = JobPost.objects.get(id=postId)
    if request.method == 'POST':
        jobpost.state = False
        jobpost.accept_candidates = False
        jobpost.save()
        return redirect('profile-jobpost-view', postId)
    context = {
        'jobpost': jobpost,
    }
    return render(request, 'core/profile_jobpost_view.html', context)

@login_required(login_url='account_login')
def profile_jobpost_edit(request, postId):
    jobpost = JobPost.objects.get(id=postId)
    jobpost_form = JobPostForm(instance=jobpost)
    if request.method == 'POST':
        jobpost_form = JobPostForm(request.POST, instance=jobpost)
        if jobpost_form.is_valid():
            jobpost_form.instance.user = request.user
            jobpost_form.save()
            return redirect('profile')
    context = {
        'jobpost_form': jobpost_form,
    }
    return render(request, 'core/jobpost_edit.html', context)

@login_required(login_url='account_login')
def profile_jobpost_delete(request, postId):
    jobpost = JobPost.objects.get(id=postId)
    print(jobpost)
    if request.method == 'POST':
        jobpost.delete()
        return redirect('profile')
    context = {
        'jobpost': jobpost,
    }
    return render(request, 'core/jobpost_delete.html', context)

@login_required(login_url='account_login')
def profile_jobpost_candidates(request, postId):
    jobpost = JobPost.objects.get(id=postId)
    
    candidates = jobpost.get_candidates
    candidates_users_arr = [ candidate.user.all() for candidate in candidates ]
    candidates_users_id_arr = [ user[0] for user in candidates_users_arr ]
    
    if request.method == 'POST':
        user = request.POST.get('userId')
        interesting_candidate = JobPostCandidate.objects.get(user=user)
        interesting_candidate.state = True
        interesting_candidate.save()
        return redirect('profile_jobpost_candidates', postId)

    nominees = jobpost.get_nominees
    nominees_users_arr = [ nominee.user.all() for nominee in nominees ]
    nominees_users_id_arr = [ user[0].id for user in nominees_users_arr ]
    context = {
        'jobpost': jobpost,
        'candidates': candidates,
        'candidates_users_id_arr': candidates_users_id_arr,
        'nominees_users_id_arr': nominees_users_id_arr,
    }
    return render(request, 'core/profile-jobpost-candidates.html', context)

@login_required(login_url='account_login')
def profile_jobpost_nominees(request, postId):
    jobpost = JobPost.objects.get(id=postId)
    nominees = jobpost.get_nominees
    hired_arr = [ i.user.all() for i in nominees if i.hired == True ]
    hired_id_arr = [ i[0].id for i in hired_arr ]
    nominees_users_arr = [ nominee.user.all() for nominee in nominees ]
    nominees_users_id_arr = [ user[0] for user in nominees_users_arr ]
    context = {
        'jobpost': jobpost,
        'nominees_users_id_arr': nominees_users_id_arr,
        'hired_id_arr': hired_id_arr,
    }
    return render(request, 'core/profile_jobpost_nominees.html', context)

@login_required(login_url='account_login')
def profile_jobpost_candidate(request, postId, userId):
    user = User.objects.get(id=userId)
    profile = Profile.objects.get(user=user)
    context = {
        'profile': profile,
    }
    return render(request, 'core/user_profile.html', context)

# @login_required(login_url='account_login')
# def profile_jobpost_nominee_hire(request, postId, nomineeId):
#     post = JobPost.objects.get(id=postId)
#     jobpost = JobPost.objects.get(id=post.id)
#     nominee = JobPostCandidate.objects.get(user=nomineeId)
#     if request.method == 'POST':
#         # jobpost.state = False
#         nominee.hired = True
#         # jobpost.save()
#         nominee.save()
#         # profile = Profile.objects.get(user=nomineeId)
#         # subject = f'{jobpost} job post'
#         # from_email = 'aymankastali1@gmail.com'
#         # message = f'Congrats, You have been nominated for {jobpost} job title\nYou will receive an email soon for an interview\n\nBest wishes'
#         # if subject and message and from_email:
#         #     send_mail(subject, message, from_email, [profile.email])
#         return redirect('profile_jobpost_nominees', postId)

@login_required(login_url='account_login')    
def set_interview_appointment(request, postId, nomineeId):
    user = User.objects.get(id=nomineeId)
    jobpost = JobPost.objects.get(id=postId)
    appointment_form = AppointmentForm()
    candidate = JobPostCandidate.objects.get(user=user)
    interview_date_post = request.POST.get('interview_date')
    interview_time_post = request.POST.get('interview_time')
    
    subject = f'{jobpost} job title interview appointment'
    from_email = 'aymankastali1@gmail.com'
    message = f'Dear {user.profile.name} \nYour interview detail will be at: {interview_date_post} at {interview_time_post} oclock \nBest wishes'
    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST, instance=candidate)
        if appointment_form.is_valid():
            appointment_form.instance.interview_date = interview_date_post
            appointment_form.instance.interview_time = interview_time_post
            appointment_form.instance.hired = True
            appointment_form.save()
            if subject and message and from_email:
                send_mail(subject, message, from_email, [user.profile.email])
                return redirect('profile_jobpost_nominees', postId)
    context = {
        'user': user,
        'appointment_form': appointment_form,
    }
    return render(request, 'core/set_interview_appointment.html', context)

@login_required(login_url='account_login')
def appointments_lst(request, postId):
    jobpost = JobPost.objects.get(id=postId)
    nominees = jobpost.get_nominees
    nominees__hired_users_arr = [ nominee.user.all() for nominee in nominees if nominee.hired == True ]
    nominees_users_id_arr = [ user[0] for user in nominees__hired_users_arr ]

    if request.method == 'POST':
        if 'hire' in request.POST:
            user = User.objects.get(id=request.POST.get('userId'))
            nominee_user =  JobPostCandidate.objects.get(user=request.POST.get('userId'))
            nominee_user.save()
            nominee_user.accepted = True
            jobpost.state = False
            jobpost.save()
            nominee_user.save()
            subject = f'{jobpost} job title Acceptance'
            from_email = 'aymankastali1@gmail.com'
            message = f'Dear {user.profile.name} \nWe would like to welcome you to our family, waiting for you to start your position at next monday at 8:00 am \nBest wishes'
            if subject and message and from_email:
                send_mail(subject, message, from_email, [user.profile.email])
            return redirect('profile_jobpost_nominees_appointments_lst', postId)
            
        elif 'add_note' in request.POST:
            nominee_user = JobPostCandidate.objects.get(user=request.POST.get('userId'))
            nominee_user.notes = request.POST.get('notes')
            nominee_user.save()
            return redirect('profile_jobpost_nominees_appointments_lst', postId)
    
    context = {
        'jobpost': jobpost,
        'nominees_users_id_arr': nominees_users_id_arr,
        'nominees': nominees,
    }
    return render(request, 'core/appointments_list.html', context)
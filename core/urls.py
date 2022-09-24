from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('save_post/<str:postId>', save_post, name='save-post-id'),
    path('save_jobpost/<str:postId>', save_jobpost, name='save-jobpost-id'),
    path('tag_add/', tag_add, name='tag-add'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/user_jobposts', user_jobposts, name='profile-user-jobposts'),
    path('accounts/profile/user_tagposts', tag_jobposts, name='profile-user-tagposts'),
    path('accounts/profile/user_tagposts/delete', tag_jobposts_delete, name='profile-user-tagposts-delete'),
    path('accounts/profile/<str:userId>/user_profile', user_profile, name='profile-id-user'),    
    path('accounts/profile/<str:userId>/user_page', user_page, name='profile-id-page'),
    path('accounts/profile/<str:userId>/user_page/posts', user_page_posts, name='profile-id-page-posts'),
    path('accounts/profile/<str:userId>/user_page/job_posts', user_page_jobposts, name='profile-id-page-jobposts'),
    path('accounts/profile/<str:userId>/user_page/job_posts/<str:jobId>/post', jobpost_view, name='profile-id-page-jobposts-id-post'),
    path('accounts/profile/<str:userId>/user_page/job_posts/<str:jobId>/post/apply', job_apply, name='profile-id-page-jobposts-id-post-apply'),

    path('accounts/profile/job_applied', jobs_applied, name='profile-jobsapplied'),
    path('accounts/profile/create_profile_or_page', create_profile_or_page, name='profile-create'),
    path('accounts/profile/edit', profile_edit, name='profile-edit'),
    path('accounts/profile/page_edit', page_edit, name='page-edit'),
    path('accounts/profile/posts', posts, name='profile-posts'),
    path('accounts/profile/saved_post', saved_posts, name='profile-savedposts'),
    path('accounts/profile/saved_jobpost', saved_jobposts, name='profile-savedjobposts'),
    
    path('accounts/profile/posts/<str:postId>/like', post_like, name='profile-posts-id-like'),
    path('accounts/profile/posts/<str:postId>/dislike', post_unlike, name='profile-posts-id-unlike'),
    path('accounts/profile/posts/<str:postId>/edit', post_edit, name='profile-posts-edit'),
    path('accounts/profile/posts/<str:postId>/delete', post_delete, name='profile-posts-delete'),
    path('accounts/profile/posts/<str:postId>/comment_add', post_comment, name='profile-posts-id-comment'),
    path('accounts/profile/posts/<str:postId>/comment/<str:commentId>/edit', post_comment_edit, name='profile-posts-id-comment-id-edit'),
    path('accounts/profile/posts/<str:postId>/comment/<str:commentId>/delete', post_comment_delete, name='profile-posts-id-comment-id-delete'),
    path('accounts/profile/posts/<str:postId>/comment/<str:commentId>/like', post_comment_like, name='profile-posts-id-comment-id-like'),
    path('accounts/profile/posts/<str:postId>/comment/<str:commentId>/unlike', post_comment_unlike, name='profile-posts-id-comment-id-unlike'),
    path('accounts/profile/posts/<str:postId>/comment/<str:commentId>/likes_page', post_comment_likes_page, name='profile-posts-id-comment-id-likespage'),
    path('accounts/profile/posts/<str:postId>/comment/<str:commentId>/reply', post_comment_reply, name='profile-posts-id-comment-id-reply'),
    path('accounts/profile/posts/<str:postId>/comment/<str:commentId>/reply/<str:replyId>/edit', post_comment_reply_edit, name='profile-posts-id-comment-id-reply-id-edit'),
    path('accounts/profile/posts/<str:postId>/comment/<str:commentId>/reply/<str:replyId>/delete', post_comment_reply_delete, name='profile-posts-id-comment-id-reply-id-delete'),
    path('accounts/profile/posts/<str:postId>/comment/<str:commentId>/reply/<str:replyId>/like', post_comment_reply_like, name='profile-posts-id-comment-id-reply-id-like'),
    path('accounts/profile/posts/<str:postId>/comment/<str:commentId>/reply/<str:replyId>/unlike', post_comment_reply_unlike, name='profile-posts-id-comment-id-reply-id-unlike'),
    path('accounts/profile/posts/<str:postId>/comment/<str:commentId>/reply/<str:replyId>/likes_page', post_comment_reply_likes_page, name='profile-posts-id-comment-id-reply-id-likes_page'),
    
    
    path('accounts/profile/connections', connections, name='profile-connections'),
    path('accounts/profile/followings', followings, name='profile-followings'),
    path('accounts/profile/requests', requests, name='profile-requests'),
    path('accounts/profile/requests/accept', connection_request_accept, name='profile-requests-accept'),
    path('accounts/profile/requests/reject', connection_request_reject, name='profile-requests-reject'),
    
    path('accounts/profile/connections/<str:userId>/', connection_profile, name='profile-connections-id'),
    path('accounts/profile/connections/add', connection_add, name='profile-connections-add'),
    path('accounts/profile/connections/<str:userId>/remove', connection_remove, name='profile-connections-id-remove'),
    path('accounts/profile/connections/<str:userId>/block', connection_block, name='profile-connections-id-block'),
    path('accounts/profile/follow', profile_follow, name='profile-follow'),
    path('accounts/profile/unfollow', profile_unfollow, name='profile-unfollow'),
    
    path('accounts/profile/follower/<str:userId>/', follower_profile, name='profile-follower-id'),
    path('accounts/profile/follower/<str:userId>/block', follower_block, name='profile-follower-id-block'),
    path('accounts/profile/followers', followers, name='profile-followers'),
    path('accounts/profile/blocks', blocks, name='profile-blocks'),

    
    path('accounts/profile/jobposts', profile_jobposts, name='profile-jobposts'),
    path('accounts/profile/jobpost_add', profile_jobpost_add, name='profile-jobpost-add'),
    path('accounts/profile/jobpost/<str:postId>/', profile_jobpost_view, name='profile-jobpost-view'),
    path('accounts/profile/jobpost/<str:postId>/candidates', profile_jobpost_candidates, name='profile_jobpost_candidates'),
    path('accounts/profile/jobpost/<str:postId>/nominees', profile_jobpost_nominees, name='profile_jobpost_nominees'),
    path('accounts/profile/jobpost/<str:postId>/nominees/appointments_lst', appointments_lst, name='profile_jobpost_nominees_appointments_lst'),
    # path('accounts/profile/jobpost/<str:postId>/nominees/<str:nomineeId>/hire', profile_jobpost_nominee_hire, name='profile-jobpost_nominee-id-hire'),
    path('accounts/profile/jobpost/<str:postId>/nominees/<str:nomineeId>/set_interview_appointment', set_interview_appointment, name='profile-jobpost_nominee-id-setinterviewappointment'),
    path('accounts/profile/jobpost/<str:postId>/candidate/<str:userId>/', profile_jobpost_candidate, name='profile-jobpost-candidate-id'),
    path('accounts/profile/jobpost/<str:postId>/edit', profile_jobpost_edit, name='profile-jobpost-edit'),
    path('accounts/profile/jobpost/<str:postId>/delete', profile_jobpost_delete, name='profile-jobpost-delete'),
    
    
]
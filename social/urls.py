from social import views as s_views
from django.urls import path

urlpatterns = [
    path('all-posts/', s_views.PostListView.as_view(), name="post-list-view"),
    path('post-delete/<post_slug>/', s_views.PostDeleteView.as_view(),
         name="post-delete-view"),
    path('user-profile/<slug:user_slug>/',
         s_views.UserProfileView.as_view(), name="profile-list-view"),
    path('post-update/<slug:post_slug>/',
         s_views.UpdatePostView.as_view(), name="update-post-view"),
    path('post-detail/<slug:post_slug>/',
         s_views.DetailPostView.as_view(), name="detail-post-view"),
    path('jobs-list/', s_views.JobsView, name="jobs-list-view"),
    path('comment-on-post/<slug:post_slug>/',
         s_views.CreateCommentPostView.as_view(), name="create-postcomment-view"),
    path('delete-comment-post/<int:comment_id>/',
         s_views.DeleteCommentPostView.as_view(), name="delete-postcomment-view"),
]

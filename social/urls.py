from social import views as s_views
from django.urls import path

urlpatterns = [
    path('all-posts/', s_views.PostListView.as_view(), name="post-list-view"),
    path('post-creation/', s_views.PostCreateView.as_view(),
         name="post-create-view"),
    path('user-profile/<slug:user_slug>/',
         s_views.UserProfileView.as_view(), name="profile-list-view"),
    path('post-update/<slug:post_slug>/',
         s_views.UpdatePostView.as_view(), name="update-post-view"),
    path('jobs-list/', s_views.JobsView, name="jobs-list-view"),
]

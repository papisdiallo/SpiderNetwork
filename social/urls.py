from social import views as s_views
from django.urls import path

urlpatterns = [
    path('all-posts/', s_views.PostListView.as_view(), name="post-list-view"),
    path('post-creation/', s_views.PostCreateView.as_view(),
         name="post-create-view"),
    path('user-profile/', s_views.UserProfile, name="profile-list-view"),
    path('jobs-list/', s_views.JobsView, name="jobs-list-view"),
]

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("", views.api_root),
    path("latest-stories/", views.StoryList.as_view(), name="lateststory-list"),
    path("latest-stories/<uuid:pk>/", views.StoryDetail.as_view(), name="lateststory-detail"),
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    path("comments/", views.CommentList.as_view(), name="comment-list"),
    path("comments/<uuid:pk>/", views.CommentDetail.as_view(), name="comment-detail"),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]

urlpatterns = format_suffix_patterns(urlpatterns)

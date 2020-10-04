from django.urls import path
from api.views import Index, UserCreate, PostList, PostListAuthorPosts, PostCreate, PostDetail, CreateComment
from rest_framework.authtoken import views

urlpatterns = [
    path("", Index.as_view(), name='index'),
    path("posts/", PostList.as_view(), name='posts'),
    path("author-posts/", PostListAuthorPosts.as_view(), name='author-posts'),
    path("post-create/", PostCreate.as_view(), name='post-create'),
    path("post-detail/<int:pk>/", PostDetail.as_view(), name="post-detail" ),
    path("create-comment/<int:pk>/", CreateComment.as_view(), name="create-comment"),
    path("create-user/", UserCreate.as_view(), name='create user'),
    path('login/', views.obtain_auth_token, name='login'),
]


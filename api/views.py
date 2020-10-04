from django.shortcuts import render
from rest_framework import permissions
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.serializers import UserSerializer, PostSerializer, PostDetailSerializer, CommentSerializer
from api.models import Post

from rest_framework.pagination import CursorPagination

class CursorSetPagination(CursorPagination):
    """
        Pagintion for 10 entities
    """
    page_size = 10
    page_size_query_param = 'page_size'
    ordering = '-timestamp' # '-created' is default

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
        Custom permission
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user

class Index(generics.ListAPIView):
    """
        Main view. Description of all the endpoints avaiables.
    """
    permission_classes = (AllowAny, )
    def get(self, request):
        api_views = {
            "Posts": "posts/",
            "Post of an logged in author": "author-posts/",
            "Create Posts": "post-create/",
            "Post detail": "post-detail/<int:pk>/",
            "Create comment": "create-comment/<int:pk>/",
            "Create user": "create-user/",
            "Log in": "login/",
        }
        return Response(api_views)

class UserCreate(generics.CreateAPIView):
    """
        Create an user.
        Needed information: username(String), password(String) and email(String).
    """
    authentication_classes = ()
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

class PostList(generics.ListAPIView):
    """
        List of all posts
        Listo of 10 first posts, next and previus.
    """
    authentication_classes = ()
    permission_classes = (AllowAny, )
    pagination_class = CursorSetPagination

    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostListAuthorPosts(generics.ListAPIView):
    """
        Retrive all post of a logged in user
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def list(self, request):
        permission_classes = (IsAuthenticated, )
        try:
            queryset = Post.objects.filter(author=request.user)
            serializer = PostSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            raise PermissionDenied({"error": "Must be logged"})

class PostCreate(generics.CreateAPIView):
    """
        Create a post
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        Detail of a post. Pk needed
    """
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

class CreateComment(generics.CreateAPIView):
    """
        Create a comment. Pk of a post needed and a user need to be logged in
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = CommentSerializer

    def post(self, request, pk):
        user = request.user.pk
        
        content = request.data.get("content") 

        data = {"user": user, "post": pk, "content": content}
        
        serializer = CommentSerializer(data=data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
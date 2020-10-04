from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from api.models import Post, Comment

class UserSerializer(serializers.ModelSerializer):
    """
        Create an user
    """

    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):

        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

class PostSerializer(serializers.ModelSerializer):
     class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ('title', 'overview', 'content', 'timestamp', 'author', 'thubnail', 'comments')
    
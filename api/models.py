from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    content = models.TextField()                                                    # Try text rich field
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    thubnail = models.ImageField(upload_to='images/', null=True, max_length=255)
    active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.title
    
    def comments(self):
        try:
            comments = self.comments.all().order_by('-timestamp')
        except:
            comments = None
        return comments

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.user.username + self.post.title

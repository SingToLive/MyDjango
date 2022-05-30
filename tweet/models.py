from django.db import models
from user.models import UserModel


# Create your models here.
class Tweet(models.Model):
    class Meta:
        db_table = "tweet"

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TweetComment(models.Model):
    class Meta:
        db_table = "comment"
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE) #트윗 번호
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE) #댓글 작성자
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
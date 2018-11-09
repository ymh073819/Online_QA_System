from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.


class auth_profile(models.Model):#User的扩展字段  一对一关系
    Personality_signature = models.CharField(max_length=50, blank=True)
    head_img = models.ImageField(upload_to='img',blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __unicode__(self):
        return self.content

class Article(models.Model):
    title = models.CharField(max_length=20,blank=False)
    author = models.CharField(max_length=10,blank=False)
    content = models.TextField(max_length=140,blank=False)
    answer_number = models.IntegerField(default=0)
    poll_number = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default='')

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    author = models.CharField(max_length=10,blank=False)
    content = models.TextField(max_length=140,blank=False)
    article_id = models.ForeignKey(Article,on_delete=models.CASCADE)
    img = models.ImageField(upload_to='img')
    new_answer = models.BooleanField(default=True)

    def __unicode__(self):
        return self.content


class Poll(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)

    def __unicode__(self):
        return self.id


class Friendship(models.Model):
    to_friend = models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_friend_set')#related_name用于反向查找即related_name作为查询条件，查询User
    from_friend = models.ForeignKey(User,on_delete=models.CASCADE)                             #同时用于区别于其他外键

    def __unicode__(self):
        return self.id






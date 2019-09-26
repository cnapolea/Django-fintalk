from django.db import models
from django.contrib.auth.models import User

class Talk(models.Model):
    """Talks will be created by admins only. These will be relevant topics related to 
Finance, where users will be able to add their own topics in order to create a conversation."""

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def has_topic(self):
        """Checks if talk has any topic and returns either True or False."""
        topic_count = self.topics.all().count()
        if topic_count <= 0:
            return False
        return True
    
    def count_topics(self):
        """Returns how many topics in the talk."""
        topic_count = self.topics.all().count()
        return topic_count
    
    def get_most_recent_topics(self):
        """Returns a list of the 3 most recent topics."""
        recent_topics = self.topics.all().order_by('-date_created')[:3]
        return recent_topics
    
class FollowTalk(models.Model):
    """FollowTalk is a many-to-many middle table, which allows users to follow as many talks
they wish and at the same time, a talk can be followed by n users."""

    user = models.ForeignKey(User, related_name='follows_talk', on_delete=models.CASCADE)
    talk = models.ManyToManyField(Talk, related_name='followers')

class Topic(models.Model):
    """User will be able to create a topic under a talk. Topic needs to be connected to Talk."""
    
    talk = models.ForeignKey(Talk, related_name='topics', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='topics', null=True)

    subject = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject
    
    def count_posts(self):
        """Returns the number of posts under this specific topic object."""
        post_count = self.posts.all().count()
        return post_count

class Post(models.Model):
    """User will create a post under a topic."""

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:280] + '...'

class LikePost(models.Model):
    """Middle table (many-to-many relationship) between a user and a topic."""

    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ManyToManyField(Post, related_name='likes')

class UserFollowUser(models.Model):
    follower = models.ForeignKey(User, related_name='follows', on_delete=models.CASCADE)
    being_followed = models.ManyToManyField(User, related_name='is_followed_by')      
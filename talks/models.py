from django.db import models
from django.contrib.auth.models import User

class Talk(models.Model):
    """Talks will be created by admins only. These will be relevant topics related to 
    Finance, where users will be able to add their own topics in order to create a conversation."""

    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-date_created"]
    
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
        recent_topics = self.topics.all().order_by('-date_created')
        
        return recent_topics
    
class FollowTalk(models.Model):
    """FollowTalk is a many-to-many middle table, which allows users to follow as many talks they wish and at the same time, a talk can be followed by n users."""

    user = models.ForeignKey(User, related_name='follows_talk', on_delete=models.CASCADE)
    talk = models.ForeignKey(Talk, related_name='followers', on_delete=models.CASCADE)

class Post(models.Model):
    """User will be able to create a post under a talk. Posts needs to be connected to Talk."""
    
    talk = models.ForeignKey(Talk, related_name='posts', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='posts', on_delete=models.SET_NULL, null=True)

    content = models.TextField() 
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.content)
    
    class Meta:
        ordering = ["-date_created"]

    def count_replies(self):
        """Returns the number of replies under this specific post object."""
        counter = self.replies.all().count()
       
        return counter
    
    def format_date(self):
        """This function helps format an unformatted datetime string to [Weekday], [month] [date] at [time]"""
        
        return self.date_created.strftime('%a, %b %d at %H:%d')

class Reply(models.Model):
    """User will create a reply under a post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')

    reply = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:100] + '...'
    
    class Meta:
        ordering = ["-date_created"]

    def format_date(self):
        """This function helps format an unformatted datetime string to [Weekday], [month] [date] at [time]"""
        
        return self.date_created.strftime('%a, %b %d at %H:%d')

class FavoriteTalk(models.Model):
    """Middle table (many-to-many relationship) between a user and a talk."""

    user = models.ForeignKey(User, related_name='favorite_talks', on_delete=models.CASCADE)
    talk = models.ForeignKey(Talk, related_name='user_favorites', on_delete=models.CASCADE)

class LikePost(models.Model):
    """Middle table (many-to-many relationship) between a user and a Post."""

    user = models.ForeignKey(User, related_name='liked_posts', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='user_post_likes', on_delete=models.CASCADE)

class LikeReply(models.Model):
    """Middle table (many-to-many relationship) between a user and a reply."""

    user = models.ForeignKey(User, related_name='liked_replies', on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, related_name='user_reply_likes', on_delete=models.CASCADE)

class UserFollowUser(models.Model):
    follower = models.ForeignKey(User, related_name='follows', on_delete=models.CASCADE)
    being_followed = models.ForeignKey(User, related_name='is_followed_by', on_delete=models.CASCADE)
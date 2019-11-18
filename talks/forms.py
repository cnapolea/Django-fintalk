from django.forms import ModelForm, Textarea
from .models import Reply, Post

class CommentForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['reply',]
        widgets = {
            'reply': Textarea(
                attrs={'placeholder':'Start     talking about this      post.',
                'class':'content-area'
                })
        }

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content',]
        widgets = {
            'content':Textarea(
                attrs = {'placeholder':'Start       writing your post.',
                'class':'content-text-ar    ea'
                })
        }
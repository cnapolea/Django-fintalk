from django.forms import ModelForm, Textarea
from .models import Reply

class CommentForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['reply',]
        widgets = {
            'reply': Textarea(attrs={
                'placeholder':'Start talking about this post.',
                'class':'content-area'
            })
        }
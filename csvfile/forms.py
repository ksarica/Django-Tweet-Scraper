from django import forms
from .models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ('author', 'date', 'text', 'comment', 'retweet', 'like')

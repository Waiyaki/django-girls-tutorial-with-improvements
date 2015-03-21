from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'title', 'text')

    def clean_author(self):
        return self.cleaned_data.get('author') or 'Anonymous'

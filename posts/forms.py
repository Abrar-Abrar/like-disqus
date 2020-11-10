from django.forms import ModelForm
from .models import Post
from django import forms


class AddPost(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'cols': 100}))

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author', 'likes', 'dislikes', )

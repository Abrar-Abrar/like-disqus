from django.forms import ModelForm
from .models import Comment
from django import forms


class AddComment(ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'cols': 100}))

    class Meta:
        model = Comment
        fields = ('content', 'image', )

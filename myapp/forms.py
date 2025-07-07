from django import forms
from .models import Photo,Category,CommentModel
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['category', 'image', 'description']

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['comment']
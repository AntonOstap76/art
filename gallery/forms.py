from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Picture,Profile,Comment


class ArtForm(forms.ModelForm):
    class Meta:
        model=Picture
        fields = ['title', 'description', 'image']
        exclude=['uploaded_by', 'uploaded_at']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Leave a comment...',
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm'
            })
        }

        
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell us a bit about yourself...',
                'class': 'w-full p-2 border rounded'
            }),
        }
from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content",)
        widgets = {
            "title": forms.TextInput(attrs={'placeholder': 'Enter the title of your post'}),
            "content": forms.Textarea(attrs={"placeholder": "Tell us something today....", "rows": 3})
        }

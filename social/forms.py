from django import forms
from .models import Post, Comment
from crispy_forms.helper import FormHelper
from django.forms.widgets import HiddenInput
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from crispy_forms.layout import (
    Layout,
    Submit,
    Row,
    Column,
    Div,
    HTML,
    Field,
    Hidden,
    Button,
    ButtonHolder,
)


class PostForm(forms.ModelForm):
    images = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True,
        })
    )

    class Meta:
        model = Post
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"placeholder": "Tell us something today....", "rows": 5, "label": ""})
        }

    def __init__(self, *args, disabled_field=True, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # self.fields["images"].widget = HiddenInput()
        self.helper = FormHelper()
        self.helper.form_id = "createPostForm"
        self.fields["content"].label = ""
        self.fields["images"].label = ""
        self.helper.layout = Layout(
            Field("content"),
            Field("images"),
            # Submit("post-create", "Post")
        )


class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"placeholder": "Comment on this post here....", "label": ""})
        }

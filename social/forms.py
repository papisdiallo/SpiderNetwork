from django import forms
from .models import Post, Comment
from crispy_forms.helper import FormHelper


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content", "images",)
        widgets = {
            "images": forms.ClearableFileInput(attrs={'multiple': True}),
            "content": forms.Textarea(attrs={"placeholder": "Tell us something today....", "rows": 3, "label": ""})
        }

    def __init__(self, *args, disabled_field=True, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # self.fields["epic_key"].widget = HiddenInput()
        self.helper = FormHelper()
        self.helper.form_id = "createPostForm"
        self.fields["content"].label = ""
        self.fields["images"].label = ""

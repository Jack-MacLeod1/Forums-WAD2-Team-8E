from django import forms
from django.contrib.auth.models import User
from forum_app.models import UserProfile, Post

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"password", "placeholder": "Enter password"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # Used for styling the form
        self.fields["username"].help_text = None
        self.fields["username"].widget.attrs["class"] = "username"
        self.fields["username"].widget.attrs["placeholder"] = "Enter username"
        self.fields["email"].widget.attrs["class"] = "email"
        self.fields["email"].widget.attrs["placeholder"] = "Enter email"


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('bio', 'picture',)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Used for styling the form
        self.fields["bio"].widget.attrs["class"] = "bio"
        self.fields["bio"].widget.attrs["placeholder"] = "Enter something short to describe you!"
        self.fields["bio"].widget.attrs["maxlength"] = "100"
        self.fields["picture"].widget.attrs["class"] = "picture"


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ('title', 'image', 'content',)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # Used for styling the form
        self.fields["title"].widget.attrs["class"] = "post-form-title"
        self.fields["title"].widget.attrs["placeholder"] = "Title"
        self.fields["content"].widget.attrs["class"] = "post-form-content"
        self.fields["content"].widget.attrs["placeholder"] = "Share your thoughts"
        self.fields["image"].widget.attrs["class"] = "post-form-image"
        self.fields["image"].widget.attrs["placeholder"] = "Drag and Drop media here!"
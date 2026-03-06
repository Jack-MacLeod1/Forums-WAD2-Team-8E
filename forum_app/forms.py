from django import forms
from django.contrib.auth.models import User
from forum_app.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"password", "placeholder": "Enter password"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
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
        self.fields["bio"].widget.attrs["class"] = "bio"
        self.fields["bio"].widget.attrs["placeholder"] = "Enter something short to describe you!"
        self.fields["bio"].widget.attrs["maxlength"] = "100"
        self.fields["picture"].widget.attrs["class"] = "picture"
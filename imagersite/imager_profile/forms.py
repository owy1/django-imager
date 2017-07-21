"""Combine standart django.contrib.auth.models and ImageProfile to create a super form."""


from django import forms
from imager_profile.models import ImagerProfile


class ImagerProfileForm(forms.ModelForm):
    """Edit user profile form."""

    def __init__(self, *args, **kwargs):
        """."""

        super(ImagerProfileForm, self).__init__(*args, **kwargs)

        self.fields['first name'] = forms.CharField(initial=self.instance.user.first_name)
        self.fields['last name'] = forms.CharField(initial=self.instance.user.last_name)
        self.fields['email'] = forms.CharField(initial=self.instance.user.email)
        del self.fields['user']

    class Meta:
        """."""

        model = ImagerProfile
        exclude = []

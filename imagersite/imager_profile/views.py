"""Profile View."""


from imager_images.models import Album
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from imager_profile.forms import ImagerProfileForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


class UserProfileView(LoginRequiredMixin, DetailView):
    """User profile."""

    template_name = "imager_profile/user_profile.html"
    model = ImagerProfile
    login_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        """User view context data."""
        user = request.user
        album_list = user.albumbuild.all()
        return self.render_to_response({"user": user, "albums": album_list})


class OthersProfileView(DetailView):
    """Other user profile."""

    template_name = "imager_profile/others_profile.html"
    model = ImagerProfile

    def get(self, request):
        """."""
        user = request.user
        others = User.objects.all().exclude(username='owy1')
        others = User.objects.all().exclude(user__username=user.username)
        album_list = Album.published_albums.all().filter(user__username=user.username)

        return self.render_to_response({"others": others, "albums": album_list})


class EditUserProfileView(LoginRequiredMixin, UpdateView):
    """User profile."""

    template_name = "imager_profile/edit_user_profile.html"
    model = ImagerProfile
    login_url = reverse_lazy("login")
    form_class = ImagerProfileForm
    success_url = reverse_lazy("/profile")

    def get_object(self):
        """User view context data."""
        return self.request.user.profile

    def form_valid(self, form):
        """User form."""
        self.object = form.save()
        self.object.user.first_name = form.cleaned_dat['First Name']
        self.object.user.last_name = form.cleaned_dat['Last Name']
        self.object.user.email = form.cleaned_dat['Email']
        self.object.user.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

"""Home Page View."""


from imager_images.models import Album
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django.shortcuts import render


def user_profile_view(request):
    """User profile."""
    user = request.user
    album_list = user.albumbuild.all()

    return render(request, "user_profile.html", {"user": user, "albums": album_list})


def others_profile_view(request, username):
    """Other user profile."""
    user = User.objects.all().exclude(username='owy1')
    user = User.objects.all().exclude(username=username)
    album_list = Album.published_albums.all().filter(user__username=username)

    return render(request, "others_profile.html", {"user": user, "albums": album_list})

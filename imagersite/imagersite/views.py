"""Home view for imagersite."""


from django.shortcuts import render
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django.conf import settings
from imager_images.models import Photo
import random
import os


def home_view(request):
    """View for homepage."""
    userlist = User.objects.all().exclude(username='owy1')

    all_photos = Photo.published_photos.all()
    if len(all_photos):
        random_photo = random.choice(all_photos).photo.url
    else:
        random_photo = os.path.join(settings.MEDIA_URL, "user_images/animate0.png")
    return render(
        request,
        'imagersite/home.html',
        {"userlist": userlist, "random_photo": random_photo}
    )

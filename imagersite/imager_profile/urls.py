"""URLs for the imager_profile app."""

from django.conf.urls import url
from . import views

app_name = 'imager_profile'


urlpatterns = [
    url(r'^$', views.UserProfileView.as_view(), name="user_profile"),
    url(r'^edit/$', views.EditUserProfileView.as_view(), name="edit_profile"),
    url(r'^(?P<username>[\w.@+-]+)$', views.OthersProfileView.as_view(), name="others_profile")
]

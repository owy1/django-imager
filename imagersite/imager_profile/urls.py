"""URLs for the imager_profile app."""

from django.conf.urls import url
from . import views

app_name = 'imager_profile'


urlpatterns = [
    url(r'^$', views.user_profile_view, name="user_profile"),
    # url(r'^profile/(?P<username>[\w.@+-]+)/$', views.others_profile_view, name="others_profile")
    url(r'^(?P<username>[\w.@+-]+)$', views.others_profile_view, name="others_profile")
]

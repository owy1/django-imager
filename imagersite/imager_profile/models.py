"""Model for Imager_profile."""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible

CAMERA_TYPE = (
    ("iphone", "iphone"),
    ("SamSung", "SamSung"),
    ("Nikon", "Nikon"),
    ("Canon", "Canon")
)

PHOTOGRAPHY_STYLE = (
    ("Color", "Color"),
    ("Black and White", "Black and White"),
    ("Portrait", "Portrait"),
    ("Landscape", "Landscape")
)

SOCIAL_STATUS = (
    ('Peasant', 'Peasant'),
    ('Royalty', "Royalty"),
    ('Merchant', 'Merchant'),
    ('Scholar', 'Scholar')
)


class ProfileManager(models.Manager):
    """Manage profiles."""

    def get_queryset(self):
        """Return all active users."""
        return super(ProfileManager, self).get_queryset().filter(user__is_active=True).all()


# Create your models here.
@python_2_unicode_compatible
class ImagerProfile(models.Model):
    """A profile for users to our applications."""

    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE
    )
    camera_type = models.CharField(
        max_length=25,
        choices=CAMERA_TYPE,
        default="iphone",
        null=True
    )
    photography_style = models.CharField(
        max_length=25,
        choices=PHOTOGRAPHY_STYLE,
        default="color",
        null=True
    )
    social_status = models.CharField(
        max_length=25,
        choices=SOCIAL_STATUS,
        default="peasant",
        null=True
    )
    location = models.CharField(max_length=255, blank=True, null=True)
    job = models.CharField(max_length=25, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    objects = models.Manager()
    active = ProfileManager()

    @property
    def is_active(self):
        """Active status."""
        return self.user.is_active

    def __repr__(self):
        """Print username."""
        return """
        username: {}
        camera_style: {}
        photography_style: {}
        social_status: {}
        """.format(self.user.username, self.camera_type, self.photography_style, self.social_status)

    # def __str__(self):
    #     """Print username."""
    #     self.__repr__()


@receiver(post_save, sender=User)
def make_profile_for_new_user(sender, **kwargs):
    """New Profile instances."""
    if kwargs['created']:
        new_profile = ImagerProfile(
            user=kwargs['instance']
        )
        new_profile.save()

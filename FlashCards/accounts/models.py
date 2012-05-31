from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from FlashCards import settings

def content_file_name(instance, filename):
    extension = filename.split('.')[1]
    name = '%d.'%instance.user.id + extension
    return '/'. join(['media','avatar', name])

class UserProfile(models.Model):
    user = models.ForeignKey(User, primary_key=True)
    message = models.TextField()
    avatar = models.ImageField(upload_to=content_file_name, default=settings.DEFAULT_AVATAR)

    def __str__(self):
        return self.user.username

    def save(self, force_insert=False, force_update=False, using=None):
        """
        Save Photo after ensuring it is not blank.  Resize as needed.
        """

        size=(152, 1000)
        if not self.user and not self.avatar:
            return

        super(UserProfile, self).save(force_insert=force_insert, force_update=force_update)

        filename = self.avatar.path
        image = Image.open(filename)

        image.thumbnail(size, Image.ANTIALIAS)
        image.save(filename)

    def getAvatarUrl(self):
        url = self.avatar.url
        if url.startswith('/'):
            return url
        else:
            return '/'+url
from django.db import models
from allauth.socialaccount.models import SocialApp
from Shop01.utils import ImageUploader
# Create your models here.

class SocialIcon(models.Model, ImageUploader):
    folder_name = 'social'
    name = models.ForeignKey(SocialApp, verbose_name='Социальная сеть')
    image = models.ImageField(upload_to=ImageUploader.make_upload_path, blank=True, verbose_name='Иконка')

    def __str__(self):
        return self.name

    def pic(self):
        if self.image:
            return '<img src = "%s" width="70" \>' % self.image.url

    pic.short_description = 'Иконка'
    pic.allow_tag = True
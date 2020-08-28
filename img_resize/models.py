from django.db import models
from .storage import OverwriteStorage
import os

class Image(models.Model):
    img = models.ImageField(upload_to="img/original")
    img_resized = models.ImageField(upload_to="img/resized", storage=OverwriteStorage(), blank=True)

    def __str__(self):
        return os.path.basename(self.img.name)

    def save(self, *args, **kwargs):
        if not self.img_resized:
            self.img_resized = self.img
        super().save(*args, **kwargs)



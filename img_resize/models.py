from django.db import models
from .storage import OverwriteStorage

class Image(models.Model):
    img = models.ImageField(upload_to="img/original")
    img_resized = models.ImageField(upload_to="img/resized", storage=OverwriteStorage(), blank=True)

    def __str__(self):
        return self.img.name.split("/")[-1]

    def save(self, *args, **kwargs):
        if not self.img_resized:
            self.img_resized = self.img
        super().save(*args, **kwargs)



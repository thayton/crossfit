from django.db import models

class CrossfitGym(models.Model):
    name = models.CharField(max_length=64)
    link = models.URLField(max_length=256, blank=True)
    addr = models.TextField()
    affid = models.PositiveIntegerField(unique=True, default=0)
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    checked_email = models.BooleanField(default=False)

    def __str__(self):
        return self.name

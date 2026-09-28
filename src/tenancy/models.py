from django.db import models

# Create your models here.

class CareHome(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

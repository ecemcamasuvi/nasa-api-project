from django.db import models

# Create your models here.

class AstronomyPicture(models.Model):
    owner=models.CharField(max_length=50,default=None, blank=True, null=True)
    title=models.CharField(max_length=75,default=None, blank=True, null=True)
    explanation=models.TextField(default=None, blank=True, null=True)
    url=models.URLField(default=None, blank=True, null=True)
    hdurl=models.URLField(default=None, blank=True, null=True)
    media_type=models.CharField(max_length=10,default=None, blank=True, null=True)
    service_version=models.CharField(max_length=10,default=None, blank=True, null=True)
    date=models.DateTimeField(default=None, blank=True, null=True)
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']

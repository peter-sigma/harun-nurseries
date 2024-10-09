from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    title = models.CharField(max_length=255, unique=True)
    image_file = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, related_name='images', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=255, unique=True)
    video_file = models.FileField(upload_to='videos/')
    category = models.ForeignKey(Category, related_name='videos', on_delete=models.CASCADE)  # One category per image
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

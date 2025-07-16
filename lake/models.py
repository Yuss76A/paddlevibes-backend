from django.db import models

class Lake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
    

class Photo(models.Model):
    lake = models.ForeignKey(Lake, related_name='photos', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='photos/')


class Review(models.Model):
    lake = models.ForeignKey(Lake, related_name='reviews', on_delete=models.CASCADE)
    user = models.CharField(max_length=50)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)

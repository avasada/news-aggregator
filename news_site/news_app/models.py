from django.db import models


# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class Headline(models.Model):
  title = models.CharField(max_length=200)
  image = models.URLField(null=True, blank=True)
  url = models.TextField()
  category = models.CharField(max_length=100)
  def __str__(self):
    return self.title
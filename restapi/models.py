from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

class ContactInfo(SingletonModel):
    github = models.CharField(max_length=2000, blank=True)
    linkedin = models.CharField(max_length=2000, blank=True)
    blog = models.CharField(max_length=2000, blank=True)
    email = models.CharField(max_length=2000, blank=True)
    phone = models.CharField(max_length=50, blank=True)

class SiteInfo(SingletonModel):
    photo_1_link = models.CharField(max_length=2000, blank=True)
    photo_2_link = models.CharField(max_length=2000, blank=True)
    photo_3_link = models.CharField(max_length=2000, blank=True)
    about = models.TextField(blank=True)

class Technology(models.Model):
    name = models.CharField(max_length=250, blank=False, unique=True)

class Project(models.Model):
    title = models.CharField(max_length=2000, blank=False)
    short_description = models.CharField(max_length=10000, blank=False)
    long_description = models.TextField()
    link = models.CharField(max_length=2000,blank=True)
    image = models.CharField(max_length=2000,blank=True)
    code_link = models.CharField(max_length=2000,blank=True)
    technologies = models.ManyToManyField("Technology", related_name="projects")
    datetime = models.DateTimeField(blank=True, null=True)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="messages")
    subject = models.CharField(max_length=1000)
    body = models.TextField()


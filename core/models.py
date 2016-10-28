from django.db import models
from datetime import datetime


class Part(models.Model):
    title = models.CharField(max_length=20)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Article(models.Model):
    part = models.ForeignKey(Part)
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=150, blank=True)
    content = models.TextField()
    create_time = models.DateTimeField(default=datetime.today())
    thumbnail = models.ImageField()
    secret = models.BooleanField(default=False)
    page_view = models.IntegerField(default=0)

    class Meta:
        ordering = ['create_time']

    def __str__(self):
        return self.title


class Appoint(models.Model):
    name = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    time = models.CharField(max_length=40, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    note = models.TextField(blank=True)
    amount = models.CharField(max_length=40, blank=True)
    finished = models.BooleanField(default=False)

    class Meta:
        ordering = ['finished']

    def __str__(self):
        return self.name + ' 的预约'


class Document(models.Model):
    title = models.CharField(max_length=60)
    desc = models.CharField(max_length=160)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    create_time = models.DateTimeField(default=datetime.today())

    class Meta:
        ordering = ['create_time']

    def __str__(self):
        return self.title

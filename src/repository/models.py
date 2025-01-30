from functools import cache

from django.db import models

# Create your models here.


class Repository(models.Model):
    id = models.IntegerField("Id")
    name = models.TextField("Name")
    full_name = models.TextField("Full Name", primary_key=True)
    forks_count = models.IntegerField("Forks")
    stargazers_count = models.IntegerField("Stars")
    watchers_count = models.IntegerField("Watchers")
    open_issues_count = models.IntegerField("Open Issues")

    @classmethod
    @cache
    def _fields_names(cls):
        return [f.name for f in Repository._meta.fields]

    @classmethod
    def build_from(cls, data):
        return Repository(**dict((field, data.get(field)) for field in cls._fields_names()))

    class Meta:
        managed = False
        verbose_name = "Repository"
        verbose_name_plural = "Repositories"

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
        # IMPORTANT: model wont be managed by Django ORM
        managed = False
        verbose_name = "Repository"
        verbose_name_plural = "Repositories"


class Recipe(models.Model):
    link = models.TextField("link", max_length=1024 * 3, primary_key=True)
    title = models.CharField("Title", max_length=1024 * 3)
    ner_length = models.TextField("NER length")
    directions_length = models.TextField("Directions length")
    ner = models.JSONField("NER")
    ingredients = models.JSONField("Ingredients")
    directions = models.JSONField("Directions")
    # source = models.TextField("Source")

    @classmethod
    @cache
    def _fields_names(cls):
        return [f.name for f in Recipe._meta.fields]

    @classmethod
    def build_from(cls, data):
        return Recipe(**dict((field, data.get(field)) for field in cls._fields_names()))

    class Meta:
        managed = False
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

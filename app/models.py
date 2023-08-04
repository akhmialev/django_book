from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20)
    pageCount = models.IntegerField()
    publishedDate = models.DateTimeField(null=True)
    thumbnailUrl = models.URLField()
    shortDescription = models.TextField()
    longDescription = models.TextField()
    status = models.CharField(max_length=20)
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

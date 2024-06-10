from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=50)


class Author(models.Model):
    full_name = models.CharField(max_length=50)


class Post(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    title = models.CharField(max_length=50)
    content = models.TextField()

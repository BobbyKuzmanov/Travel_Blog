from django.contrib.auth import get_user_model
from django.db import models
from Travel_blog.app.validators import year_validator

UserModel = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Destination(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=False)
    country = models.CharField(max_length=50, blank=False)
    year = models.IntegerField(
        blank=False,
        validators=(year_validator,))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='destinations')
    image = models.ImageField(upload_to='destinations')
    user = models.ForeignKey(
        UserModel,
        editable=False,
        on_delete=models.CASCADE)


class Like(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    field = models.CharField(max_length=2)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)


class Comment(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

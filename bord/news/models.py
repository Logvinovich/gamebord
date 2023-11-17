from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Author(models.Model):
    authoruser = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.authoruser}"


class Category(models.Model):
    name_category = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name_category}"

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    createpost_datetime = models.DateTimeField(auto_now_add=True)
    head_text = models.CharField(max_length=255, default="Заголовок")
    body_text = models.TextField()
    category = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        return self.body_text[0:123] + '...'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def __str__(self):
        return f'{Post.objects.get(pk=self.pk).get_choise_display()}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

class Comment(models.Model):
    comment_text = models.TextField()
    createcom_datetime = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    userpost = models.ForeignKey(User, on_delete=models.CASCADE)
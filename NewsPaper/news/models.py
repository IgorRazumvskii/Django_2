from django.db import models
from django.contrib.auth.models import User


CHOICES = [
    ("AR", 'article'),
    ("NE", 'news'),
]


class Author(models.Model):
    rate = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        self.rate += Post.rate_of_post * 3
        self.rate += Comment.rate_of_comment
        self.rate += self.post_set.all()
        self.save()


class Category(models.Model):
    name_of_category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article_or_news = models.CharField(max_length=2, choices=CHOICES)
    date_and_time = models.DateTimeField(auto_now=True)
    header = models.CharField(max_length=255)
    text = models.TextField()
    rate_of_post = models.IntegerField(default=0)

    category = models.ManyToManyField(Category, through='PostCategory')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def like(self):
        self.rate_of_post += 1
        self.save()

    def dislike(self):
        self.rate_of_post -= 1
        self.save()

    def preview(self):
        return self.text[:124:]+"..."


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    date_and_time = models.DateTimeField(auto_now_add=True)
    rate_of_comment = models.FloatField()

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rate_of_comment += 1
        self.save()

    def dislike(self):
        self.rate_of_comment -= 1
        self.save()


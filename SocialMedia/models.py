import datetime
from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from Users.models import User

def books_image_directory_path(instance, filename):
    now = datetime.datetime.now()
    extension = filename.split('.')[-1]
    return 'book/{0}/{1}'.format(str(now.day) + '-' + str(now.month) + '-' + str(now.year), str(uuid4()) + '.' + extension)

def author_image_directory_path(instance, filename):
    now = datetime.datetime.now()
    extension = filename.split('.')[-1]
    return 'author/{0}/{1}'.format(str(now.day) + '-' + str(now.month) + '-' + str(now.year), str(uuid4()) + '.' + extension)


class Book(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    description = models.CharField(max_length=1000)
    genres = models.CharField(max_length=400)
    image = models.ImageField(upload_to=books_image_directory_path, blank=True, null=True)
    rated_by = models.ManyToManyField(User, through='SocialMedia.Rating', related_name='users_rated')
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def update_average_rating(self):
        self.average_rating = self.rating_set.exclude(rating=0).aggregate(average=Avg('rating'))['average']
        self.save()


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.book.update_average_rating()

    class Meta:
        unique_together = ['user', 'book']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now())

class Author(models.Model):
    full_name = models.CharField(max_length=100)
    biography = models.TextField()
    birth_date = models.DateField()
    country = models.CharField(max_length=100)
    books_written = models.ManyToManyField(Book, related_name='authors')
    image = models.ImageField(upload_to=author_image_directory_path, blank=True, null=True)


    def __str__(self):
        return self.full_name


class FavoriteBook(models.Model):
    STATUS_CHOICES = (
        ('READ', 'خوانده شده'),
        ('TO_READ', 'برای خواندن'),
        ('READING', 'درحال خواندن'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TO_READ')

    def __str__(self):
        return f"{self.user.full_name} - {self.book.name} ({self.get_status_display()})"
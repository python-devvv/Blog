from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
import secrets
from django.urls import reverse


class Post(models.Model):
	title = models.CharField(max_length=100, verbose_name = "Post title")
	content = models.TextField(verbose_name = "Post content")
	date_posted = models.DateTimeField(default=timezone.now, verbose_name = "Date posted")
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "author")
	slug = models.SlugField(max_length=200, unique=True)
	bookmark = models.ManyToManyField(User, related_name='bookmark', blank=True)
	like = models.ManyToManyField(User, related_name='like', blank=True)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug ="%s-%s" %(slugify(self.title, allow_unicode=True), secrets.token_hex(10))
		return super(Post, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'slug': self.slug})
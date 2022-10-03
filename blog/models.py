from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField
import secrets
from django.urls import reverse

# adding Unique constrain to email in User model
User._meta.get_field('email')._unique = True     


class Post(models.Model):
	title = models.CharField(max_length=100, verbose_name = "Post title")
	content = RichTextField(verbose_name = "Post content")
	date_posted = models.DateTimeField(default=timezone.now, verbose_name = "Date posted")
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "author")
	slug = models.SlugField(max_length=200, unique=True)
	bookmark = models.ManyToManyField(User, related_name='bookmark', blank=True, null=True)
	like = models.ManyToManyField(User, related_name='like', blank=True, null=True)
	updated_date = models.DateTimeField(auto_now=True, verbose_name="Updated date") # Adding updated date

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			# Updating slug to more unique with the combination of multiple values
			self.slug =f"{slugify(self.title+self.author+self.content[:10], allow_unicode=True)}-{secrets.token_hex(40)}"
		return super(Post, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'slug': self.slug})

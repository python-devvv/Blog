from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(default='', null=True, blank=True)
	profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
	follow = models.ManyToManyField(User, related_name='follow', blank=True)


	def __str__(self):
		return f'{self.user.username} Profile'

	def get_absolute_url(self):
		return reverse('profile', kwargs={'username': self.user.username})


	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.profile_pic.path)
		# Resize into 350 pixel
		img_height = 350
		img_width = 350
		if img.height > img_height or img.width > img_width:
			output_size = (img_height, img_width)
			img.thumbnail(output_size)
			img.save(self.profile_pic.path)

class Feedback(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	subject = models.CharField(max_length=30)
	feedback = models.TextField(default='', null=True, blank=False)

	def __str__(self):
		return f"{self.user.username}'s Feedback | {self.subject}"

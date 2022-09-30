# from django.db.models.signals import pre_save
# from django.contrib.auth.models import User
# from django.utils import slugify
# from django.dispatch import receiver
# from .models import Post



# def create_slug(instance, new_slug=None):
# 	slug = slugify(instance.title)
# 	if new_slug is not None:
# 		slug = new_slug
# 	qs = Post.objects.filter(slug=slug).order_by('-id')
# 	if qs.exists():
# 		new_slug = "%s-%s" %(slug, qs.first().id)
# 		return create_slug(instance, new_slug=new_slug)
# 	return slug

# @receiver(pre_save, sender=Post)
# def pre_save_post_receiver(sender, instance, *args, **kwargs):
# 	if not instance.slug:
# 		instance.slug = create_slug(instance)
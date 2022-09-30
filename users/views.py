from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, ProfileUpdateForm, FeedbackForm
from .models import Profile
from django.contrib.auth.models import User
from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.template.loader import render_to_string

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'You are now able to login!!')
			return redirect('login')
	else:
		form = UserRegisterForm()

	return render(request, 'users/register.html', {'form': form, 'title' : 'Blog | Register'})

def profiles(request, username):
	p_user = get_object_or_404(User, username=username)
	profile = get_object_or_404(Profile, user=p_user)

	posts = Post.objects.filter(author=p_user)
	like_count = posts.aggregate(Count('like'))['like__count']
	author_top_posts = posts.annotate(num_likes=Count('like')).order_by('-num_likes')
	following = Profile.objects.filter(follow=p_user)
	title = "Blog | Profile - {}".format(p_user)

	#Follow logic 

	is_follow = False
	if profile.follow.filter(id=request.user.id).exists():
		is_follow = True

	context ={
	'profile' : profile,
	'posts' : posts,
	'like_count' : like_count,
	'author_top_posts' : author_top_posts,
	'is_follow' : is_follow,
	'following' : following,
	'title' : title

	}

	return render (request, 'users/profile.html', context)

@login_required
def edit_profile(request):

	p_user = get_object_or_404(User, username=request.user)
	profile = get_object_or_404(Profile, user=p_user)

	if request.method == "POST":
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if p_form.is_valid():
			p_form.save()
			messages.success(request, f'Your profile has been updated successfully!!')
			return redirect('edit-profile')
	else:
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {		
		'p_form' : p_form,
		'profile' : profile,
		'title' : 'Blog | Edit-profile'
	}

	return render(request, 'users/edit_profile.html', context)


@login_required
def follow_profile(request, username):
	
	p_user = get_object_or_404(User, username=username)
	profile = get_object_or_404(Profile, user=p_user)

	is_follow = False
	if profile.follow.filter(id=request.user.id).exists():
		is_follow = True

	if profile.follow.filter(id=request.user.id).exists():
		profile.follow.remove(request.user)
	else:
		profile.follow.add(request.user)
	# return HttpResponseRedirect(profile.get_absolute_url()) 

	if request.is_ajax():
		context = {
		'profile' : profile,
		'is_follow' : is_follow
		}
		html = render_to_string('users/profile_util.html', context, request=request)
		return JsonResponse({'form': html})
	else:
		raise Http404("Access denied!")

@login_required
def my_bookmarks(request):
	user = request.user
	bookmarks_qs = user.bookmark.all()
	bookmarks = list(reversed(bookmarks_qs))

	context={
	'posts': bookmarks,
	'title' : 'Blog | Bookmarks'
	}

	return render (request, 'users/my_bookmarks.html', context)

def top_authors(request):
	
	profiles = Profile.objects.all().annotate(num_follow=Count('follow')).order_by('-num_follow')[:5]

	context={
	'profiles': profiles,
	'title' : 'Blog | Top-authors'
	}

	return render (request, 'users/top_authors.html', context)

@login_required
def feedback(request):
	if request.method == 'POST':
		form = FeedbackForm(request.POST)

		if form.is_valid():
			# print(form.cleaned_data)
			fs = form.save(commit=False)
			feedback = form.cleaned_data.get('feedback')
			fs.user = request.user
			fs.save()
			messages.success(request, f'Thanks for your feedback!!')
			return redirect('home')
	else:
		form = FeedbackForm()

	return render(request, 'users/feedback.html', {'form': form, 'title' : 'Blog | Feedback'})
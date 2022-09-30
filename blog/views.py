from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.views.generic import ListView
from .forms import NewPostForm, PostEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.db.models import Count, Q
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.paginator import Paginator


def home(request):

	qs = Post.objects.all().order_by('-date_posted')
	paginator = Paginator(qs, 5)

	page_number = request.GET.get('page')
	posts = paginator.get_page(page_number)
	context = {
	'posts' : posts,
	'title' : 'Blog | Home'
	}
	return render(request, 'blog/home.html', context)

@login_required
def new_post(request):
	if request.method == "POST":
		form = NewPostForm(request.POST)
		if form.is_valid():
			current_user = User.objects.get(id=request.user.id)
			instance = form.save(commit=False)
			instance.author = current_user
			instance.save()
			title = form.cleaned_data.get('title')
			return redirect('home')
	else:	
		form = NewPostForm()
	return render(request, 'blog/new_post.html', {'form':form, 'title' : 'Blog | New-post'})

def post_detail(request, slug):
	post = get_object_or_404(Post, slug=slug)
	title = "Blog | {}".format(post.title)

	# Bookmark logic
	is_bookmark = False
	if post.bookmark.filter(id=request.user.id).exists():
		is_bookmark = True

	# Like logic
	is_like = False
	if post.like.filter(id=request.user.id).exists():
		is_like = True

	context = {
	'post' : post,
	'is_bookmark' : is_bookmark,
	'is_like' : is_like,
	'title' : title
	}

	return render(request, 'blog/post_detail.html', context)

@login_required
def edit_post(request, slug):
	post = get_object_or_404(Post, slug=slug)

	if post.author == request.user:

		if request.method == 'POST':

			edit_form = PostEditForm(request.POST, instance=post)
			if edit_form.is_valid():
				edit_form.save()
				messages.success(request, f'Your changes has been updated successfully!!')
				return HttpResponseRedirect(post.get_absolute_url())
		else:
			edit_form=PostEditForm(instance=post)
	else:
		return HttpResponseRedirect(post.get_absolute_url())
		
	context = {
	'edit_form' : edit_form,
	'title' : 'Blog | Edit-post'
	}

	return render(request, 'blog/edit_post.html', context)

@login_required
def delete_post(request, slug):
	post = get_object_or_404(Post, slug=slug)
	if post.author == request.user:
		post.delete()
		messages.success(request, f'Your post has been deleted successfully!!')
		return redirect('home')
	else:
		return HttpResponseRedirect(post.get_absolute_url())


@login_required
def bookmark_post(request, slug):
	post = get_object_or_404(Post, slug=slug)
	if post.bookmark.filter(id=request.user.id).exists():
		post.bookmark.remove(request.user)
		messages.success(request, f'This post is successfully removed from your Bookmarks!!')
	else:
		post.bookmark.add(request.user)
		messages.success(request, f'This post is successfully added to your Bookmarks!!')
	return HttpResponseRedirect(post.get_absolute_url())

@login_required
def like_post(request, slug):
	post = get_object_or_404(Post, slug=slug)

	# Like logic
	is_like = False
	if post.like.filter(id=request.user.id).exists():
		is_like = True

	if post.like.filter(id=request.user.id).exists():
		post.like.remove(request.user)
	else:
		post.like.add(request.user)
	# return HttpResponseRedirect(post.get_absolute_url())
	if request.is_ajax():
		context = {
		'post' : post,
		'is_like' : is_like
		}
		html = render_to_string('blog/post_util.html', context, request=request)
		return JsonResponse({'form': html})
	else:
		raise Http404("Access denied!")

def top_posts(request):
	posts = Post.objects.annotate(num_likes=Count('like')).order_by('-num_likes')[:5]

	context = {
	'posts' : posts,
	'title' : 'Blog | Top-posts'
	}

	return render(request, 'blog/top_posts.html', context)

def search(request):
	search_query = request.GET.get('user_search_input')

	if search_query:
		results = Post.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query)).order_by('-date_posted')
	else:
		return HttpResponse("Access denied")
	context={
	'results' : results,
	'search_word' : search_query
	}
	return render(request, 'blog/search.html', context)
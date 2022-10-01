from django.urls import path, include
from .views import profiles, follow_profile, register, edit_profile, my_bookmarks, top_authors, feedback
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('<str:username>/', profiles, name='profile'),
    path('<str:username>/follow-profile', follow_profile, name='follow-profile'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('edit-profile/', edit_profile, name='edit-profile'),
    path('bookmarks/', my_bookmarks, name='bookmarks'),
    path('top-authors/', top_authors, name='top-authors'),
    path('feedback/', feedback, name='feedback'),
    path('profile/', include('users.urls')),

 ]

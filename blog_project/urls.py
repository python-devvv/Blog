from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import register, edit_profile, my_bookmarks, top_authors, feedback
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('edit-profile/', edit_profile, name='edit-profile'),
    path('bookmarks/', my_bookmarks, name='bookmarks'),
    path('top-authors/', top_authors, name='top-authors'),
    path('feedback/', feedback, name='feedback'),
    path('', include('blog.urls')),
    path('profile/', include('users.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
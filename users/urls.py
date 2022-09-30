from django.urls import path
from .views import profiles, follow_profile

urlpatterns = [

    path('<str:username>/', profiles, name='profile'),
    path('<str:username>/follow-profile', follow_profile, name='follow-profile'),

 ]
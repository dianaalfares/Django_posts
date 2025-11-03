from django.urls import path 
from . import views 



from .views import *

urlpatterns = [
    path('hello/',views.register),
     path('login/',views.Login),
     path('getprof/',views.get_profile),
     path('read_posts/',views.read_posts),
    path('create_post/',views.create_post),
    #  path('update_post/',views.update_post),
     path('delet_post/',views.delet_post),
]



# register 
# login
# get profile for  one user 
# read posts for all persons
# create post for one user
# update post for one user
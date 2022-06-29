from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login',views.login),
    path('add',views.register),
    path('home',views.success),
    path('home/stat',views.stat),
    path('home/addwish',views.addwishform),
    path('home/makewish',views.addwish),
    path('logout',views.logout),
    path('home/edit/<_id>',views.editt),
    path('home/edit/<_id>/e',views.editwish),
    path('home/del/<_id>',views.dle),
    path('home/Granted/<_id>',views.Granted),
    path('like/<_id>',views.like_wish),
]
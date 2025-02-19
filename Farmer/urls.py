from django.urls import path
from .import views

urlpatterns=[
    path('index',views.index,name="home"),
    path('register',views.register,name="regpage"),
    path('login',views.login,name="loginpage"),
    path('about',views.about,name="aboutpage"),
    path('logout',views.logout,name="logout"),
    path('data',views.data,name="data"),
    path('recommend',views.recommend,name="recommend"),
    path('fdata',views.fdata,name="fdata"),
    path('frecommend',views.frecommend,name="frecommend")
]
# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 16:20
# @Author  : flyfish
# @Email   : im@flyfish.im

# from django.contrib import admin
# from django.urls import path，include
# from myapp import views
#
# urlpatterns = {
#     path(r'bb/', views.index,name="index"),
# }

# from django.contrib import admin
# from django.urls import path, include
# from . import views
# urlpatterns = {
#     path('', hello.index),   # 访问mysite的欢迎页
#     path('admin/', admin.site.urls),
#     path('myapp/', include("myapp.urls"))#包含blog应用中的urls
# }

from django.urls import path

from . import views

app_name = 'myapp'

urlpatterns = {
    path('index/', views.index),
    path('home/', views.home),
}
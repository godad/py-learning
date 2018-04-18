# -*- coding: utf-8 -*-
# @Time    : 2018/4/18 10:56
# @Author  : flyfish
# @Email   : im@flyfish.im

from django.shortcuts import render
from django.http import HttpResponse
# 此页面处理项目首页内容

def index(request):
    return HttpResponse("Hello, python！")
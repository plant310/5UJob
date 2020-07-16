"""myWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from myApp import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    url(r'^$',views.index),
    url('index', views.index,name='index'),
    url('get_proId/',views.getProId,name='get_proId'),
    url('get_analysis/', views.getAnalysis,name='get_analysis'),
    url('salary_forecast/', views.salary_forecast,name='salary_forecast'),
    url('region_forecast/',views.region_forecast,name='region_forecast'),
    url('predict',views.predict,name='predict'),
    url('login',views.login,name='login'),
    # url(r'^analysis/(?P<param>\w+)/$', views.analysis, name='analysis'),
    url(r'^analysis/pid=(?P<pid>\d+)$', views.analysis, name='analysis'),
    #url(r'analysis.*\?pid=[0-9]*',views.analysis,name='analysis'),
    url('selfcenter',views.selfcenter, name='selfcenter'),

]

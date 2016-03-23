"""Facepad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from django.contrib import admin

from facepad_app import views

from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login, name='login'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^likes/', views.like, name='like'),
    url(r'^comment/', views.comment, name='comment'),

    url(r'^portal/', views.portal, name='portal'),
    url(r'^section/(?P<id>\d+)/', views.view_post, name='view_post'),
    url(r'^add_friend/', views.add_friend, name='add_friend'),
    url(r'^send_message/(?P<id>\d+)/', views.message, name='message'),
    url(r'^post/', views.create_post, name='post'),
    url(r'^logout/', views.logout, name='logout'),


    url(r'^$', views.index, name='index'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

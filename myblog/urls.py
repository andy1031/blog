"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from blog import views
from django.views.static import serve
from django.conf import settings
from blog import urls as blog_urls   # 注意重命名

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^index/', views.index),

    url(r'^register/', views.register),
    url(r'^check_name/', views.check_name),
    url(r'^blog/', include(blog_urls)),


    # media文件的对应关系     （stacic系统自动做了相关工作）
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'^get_valid_img.png/', views.get_valid_img),
    url(r'^upload/', views.upload),

]

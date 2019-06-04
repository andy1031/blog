from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^comment/', views.comment),
    url(r'^add_article/', views.add_article),
    url(r'^comment_tree/(\d+)', views.comment_tree),
    url(r'^up_down/', views.up_down),   # 函数有参数时，要使用分组匹配
    url(r'^(\w+)/article/(\d+)', views.article_detail),  # 两个分组向函数传递两个参数

    url(r'^(\w+)', views.home),   # 函数有参数时，要使用分组匹配


]

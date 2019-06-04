from django import template
from blog import models
from django.db.models import Count

register = template.Library()
@register.inclusion_tag('left_menu.html')
def get_left_menu(username):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog  # 根据uer找到blog
    # ==========文章分类========
    category_list=models.Category.objects.filter(blog=blog).annotate(c=Count('article')).values('title','c')
    # ==========文章标签========
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count('article')).values('title','c')
    # ==========文章发布时间=======  时间格式化
    archive_list = models.Article.objects.filter(user=user).extra(
        select={'date':"date_format(create_time,'%%Y-%%m')"}  # 对crete_time字段格式化，赋值给c
    ).values('date').annotate(c=Count(1)).values('date','c')
    return {'category_list':category_list,
            'tag_list':tag_list,
            'archive_list':archive_list
            }



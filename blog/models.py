from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    '''用户信息'''
    nid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to="avatars/", default="avatars/default.png", verbose_name="头像") # 保存用户头像路径
    create_time = models.DateTimeField(auto_now_add=True)

    blog = models.OneToOneField(to="Blog",null=True)  # 一对一关联博客的信息

    def __str__(self):
        return self.username

    class Meta:
        # db_table = 'bolg'  #  强制设置表名
        verbose_name = '用户列表'   #  设置后台的表明
        verbose_name_plural = verbose_name   #  设置后台的表明复数形式


class Blog(models.Model):
    """博客信息"""
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)  # 个人博客标题
    site = models.CharField(max_length=32, unique=True)  # 个人博客url后缀
    theme = models.CharField(max_length=32)  # 博客主题

    def __str__(self):
        return self.title

    class Meta:
        # db_table = 'bolg'  #  强制设置表名
        verbose_name = '个人博客'   #  设置后台的表明
        verbose_name_plural = verbose_name   #  设置后台的表明复数形式

class Category(models.Model):
    """个人博客文章分类"""
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)  # 分类名
    blog = models.ForeignKey(to="Blog")  # 外键关联博客，一个博客站点可以有多个分类

    def __str__(self):
        return '{}-{}'.format(self.title,self.blog.title)

    class Meta:
        unique_together = ('title','blog')
        # db_table = 'bolg'  #  强制设置表名
        verbose_name = '文章分类'   #  设置后台的表明
        verbose_name_plural = verbose_name   #  设置后台的表明复数形式


class Tag(models.Model):
    """标签"""
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)  # 标签名
    blog = models.ForeignKey(to="Blog")  # 外键关联博客，一个博客站点可以有多个分类

    def __str__(self):
        return '{}-{}'.format(self.title,self.blog.title)

    class Meta:
        unique_together = ('title', 'blog')
        # db_table = 'tag  #  强制设置表名
        verbose_name = '标签'   #  设置后台的表明
        verbose_name_plural = verbose_name   #  设置后台的表明复数形式

class Article(models.Model):
    """文章概述"""
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)  # 文章标题
    desc = models.CharField(max_length=255)  # 文章描述
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间

    # 评论数
    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    # 点赞数
    up_count = models.IntegerField(verbose_name="点赞数", default=0)
    # 踩
    down_count = models.IntegerField(verbose_name="踩数", default=0)

    category = models.ForeignKey(to="Category", to_field="nid", null=True)  # 文字分类
    user = models.ForeignKey(to="UserInfo", to_field="nid")  #文章作者
    tags = models.ManyToManyField(  # 中介模型（手动创建第三章表多对多关联）
        to="Tag",
        through="Article2Tag",
        through_fields=("article", "tag"),  # 注意顺序！！！
    )

    def __str__(self):
        return self.title

    class Meta:
        # db_table = 'bolg'  #  强制设置表名
        verbose_name = '文章概要'   #  设置后台的表明
        verbose_name_plural = verbose_name   #  设置后台的表明复数形式


class ArticleDetail(models.Model):
    """文章详情表"""
    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to="Article", to_field="nid")

    def __str__(self):
        return self.article.title

    class Meta:
        # db_table = 'bolg'  #  强制设置表名
        verbose_name = '文章详情'   #  设置后台的表明
        verbose_name_plural = verbose_name   #  设置后台的表明复数形式


class Article2Tag(models.Model):
    """文章和标签的多对多关系表"""
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid")
    tag = models.ForeignKey(to="Tag", to_field="nid")

    def __str__(self):
        return '{}-{}'.format(self.article.title,self.tag.title)

    class Meta:
        unique_together = (("article", "tag"),)  # 联合唯一
        verbose_name = '文章-标签'  # 设置后台的表明
        verbose_name_plural = verbose_name  # 设置后台的表明复数形式


class ArticleUpDown(models.Model):
    """点赞表"""
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo", null=True)
    article = models.ForeignKey(to="Article", null=True)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = (("article", "user"),)   # 联合唯一
        verbose_name = '点赞'  # 设置后台的表明
        verbose_name_plural = verbose_name  # 设置后台的表明复数形式


class Comment(models.Model):
    """评论表"""
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid")
    user = models.ForeignKey(to="UserInfo", to_field="nid")
    content = models.CharField(max_length=255)  # 评论内容
    create_time = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey("self", null=True ,blank=True)  #blank=True Django damin里面也可以为空

    def __str__(self):
        return self.content

    class Meta:
        # db_table = 'bolg'  #  强制设置表名
        verbose_name = '评论'   #  设置后台的表明
        verbose_name_plural = verbose_name   #  设置后台的表明复数形式
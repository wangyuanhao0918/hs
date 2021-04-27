from django.db import models
from django.utils import timezone


# Create your models here.


class User(models.Model):
    """
    用户表
    """
    name = models.CharField(max_length=32, verbose_name='姓名', blank=True, null=True)
    phone = models.CharField(max_length=32, verbose_name='手机号', db_index=True)
    head_img = models.TextField(verbose_name='头像', blank=True, null=True)
    email = models.CharField(max_length=255, verbose_name='邮箱')
    password = models.CharField(max_length=255, verbose_name='密码')
    role_id = models.IntegerField(verbose_name='角色id', blank=True, null=True)
    sex = models.IntegerField(default=1, verbose_name='性别 /1男/2女')
    store_id = models.IntegerField(verbose_name='所属门店id', blank=True, null=True)
    group_id = models.IntegerField(verbose_name='组id', blank=True, null=True)
    is_delete = models.BooleanField(default=True, verbose_name='是否使用')
    enter_the_industry = models.DateTimeField(default=timezone.now, verbose_name='入行日期')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        db_table = 'user_staff'


class UserRole(models.Model):
    """
    用户角色表
    """
    role_name = models.CharField(max_length=100, verbose_name='角色名称')
    role_desc = models.TextField(verbose_name='角色描述', blank=True, null=True)
    is_delete = models.BooleanField(default=True, verbose_name='是否使用')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        db_table = 'user_role'


class UserPerm(models.Model):
    """
    用户权限表
    """
    url = models.CharField(max_length=255, verbose_name='URL')
    method = models.CharField(max_length=10, verbose_name='请求方法')
    desc = models.CharField(max_length=255, blank=True, null=True, verbose_name='描述')
    is_delete = models.BooleanField(default=True, verbose_name='是否使用')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        db_table = 'user_permission'


class UserRolePerm(models.Model):
    """
    用户角色权限关系表
    """
    role_id = models.IntegerField(verbose_name='角色id')
    perm_id = models.IntegerField(verbose_name='权限id')
    is_delete = models.BooleanField(default=True, verbose_name='是否使用')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        db_table = 'user_role_permission'

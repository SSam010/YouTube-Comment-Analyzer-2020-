from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class ChannelAdd(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True, db_index=True, verbose_name='SLUG')
    channel_url = models.TextField(unique=True, verbose_name='Channel link')
    channel_name = models.TextField(unique=True, verbose_name='Channel name')
    channel_desc = models.TextField(blank=True, null=True, verbose_name='Channel description')
    photo = models.ImageField(blank=True, upload_to="photos/%Y/%m/%d/", verbose_name='Photo')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Publication date')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Last edit date')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "ChannelAdd"
        verbose_name = 'Suggestion'
        verbose_name_plural = 'Suggestions'

    def get_absolute_url(self):
        return '/news/create'

    def __str__(self):
        return self.channel_name


class Channel(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    channel_url = models.TextField(unique=True)
    channel_name = models.TextField(unique=True)
    channel_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'channel'
        verbose_name = 'channel'
        verbose_name_plural = 'channels'


class Chen0(models.Model):
    channel_id = models.ForeignKey(Channel, on_delete=models.PROTECT)
    video_id = models.IntegerField(blank=True, null=True)
    com = models.TextField(blank=True, null=True)
    us = models.TextField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chen0'


class Chen1(models.Model):
    channel_id = models.ForeignKey(Channel, on_delete=models.PROTECT)
    video_id = models.IntegerField(blank=True, null=True)
    com = models.TextField(blank=True, null=True)
    us = models.TextField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chen1'


class Chen2(models.Model):
    channel_id = models.ForeignKey(Channel, on_delete=models.PROTECT)
    video_id = models.IntegerField(blank=True, null=True)
    com = models.TextField(blank=True, null=True)
    us = models.TextField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chen2'


class VidDate0(models.Model):
    channel_id = models.ForeignKey(Channel, on_delete=models.PROTECT)
    video_id = models.IntegerField(blank=True, null=True)
    load_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vid_date0'


class VidDate1(models.Model):
    channel_id = models.ForeignKey(Channel, on_delete=models.PROTECT)
    video_id = models.IntegerField(blank=True, null=True)
    load_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vid_date1'


class VidDate2(models.Model):
    channel_id = models.ForeignKey(Channel, on_delete=models.PROTECT)
    video_id = models.IntegerField(blank=True, null=True)
    load_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vid_date2'

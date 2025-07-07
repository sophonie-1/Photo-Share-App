from django.contrib import admin
from .models import Category, Photo,CommentModel
admin.site.register([Category, Photo,CommentModel])
# Register your models here.

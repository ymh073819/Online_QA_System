from django.contrib import admin

# Register your models here.
from book.models import Article
admin.site.register(Article)
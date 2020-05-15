from django.contrib import admin

from .models import MyUser, MyContent, PageRandCode

# Register your models here.

admin.site.register(MyUser)
admin.site.register(MyContent)
admin.site.register(PageRandCode)
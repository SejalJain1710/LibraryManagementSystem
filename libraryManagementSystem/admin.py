from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(Transaction)
from django.contrib import admin
from facepad_app.models import *


# Register your models here.

class AdminLike(admin.StackedInline):
    model = Likes
    extra = 3


class AdminSimpleUser(admin.ModelAdmin):
    filter_horizontal = ["friend"]


class AdminPost(admin.ModelAdmin):
    inlines = [AdminLike]
    list_display = ["__str__", "date", "user", "section"]


class AdminComment(admin.ModelAdmin):
    inlines = [AdminLike]
    list_display = ["__str__", "date", "user", "post", "count"]


class AdminSection(admin.ModelAdmin):
    pass


class AdminMessage(admin.ModelAdmin):
    pass


admin.site.register(SimpleUser, AdminSimpleUser)
admin.site.register(Post, AdminPost)
admin.site.register(Comment, AdminComment)
admin.site.register(Section, AdminSection)
admin.site.register(Message, AdminMessage)

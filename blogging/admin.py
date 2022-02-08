from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from blogging.models import Post, Category

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    # fk_name = "posts"

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    fields = ('name', 'text',)

class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = [
        CategoryInline,
    ]

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
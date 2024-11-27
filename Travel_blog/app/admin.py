from django.contrib import admin
from Travel_blog.app.models import Destination, Comment, Category


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'category', 'user')  
    list_filter = ('category', 'country')  
    search_fields = ('title', 'description')  
    ordering = ('title',)  
    inlines = (CommentInLine,)  


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

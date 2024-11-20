from django.contrib import admin
from Travel_blog.app.models import Destination, Comment, Category


class CommentInLine(admin.StackedInline):
    model = Comment


class DestinationAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'year')
    inlines = (CommentInLine, )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


admin.site.register(Destination, DestinationAdmin)

from django.contrib import admin
from .models import Language, Post


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('body_html',)
    list_filter = ('published', 'author', 'date', 'importance')
    search_fields = (
            'title', 'body', 'author', 'created_by_username',
            'modified_by_username', 'published_by_username',
            'excerpt')
    list_display = (
            'slug', 'title', 'author', 'date', 'tags', 'importance',
            'published', 'expires_at', 'created_at', 'created_by')

    def save_model(self, request, obj, form, change):
        obj.body_html = obj.render_body()
        return super().save_model(request, obj, form, change)

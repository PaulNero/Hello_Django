from django.contrib import admin, messages
from .models import Post, Comment, Category, Tags
from app_users.models import Profile


# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    max_num = 1
    min_num = 0
    fields = ['author', 'content', 'created_at']
    readonly_fields = ['created_at']

# Действие для публикации
def make_published(post, request, queryset):
    updated = queryset.update(status=Post.POST_STATUS_CHOICES[1][0], author=request.user)
    post.message_user(request, f"{updated} постов было опубликовано.", messages.SUCCESS)
    make_published.short_description = "Опубликовать выбранные посты"

# Действие для снятия с публикации
def make_unpublished(post, request, queryset):
    updated = queryset.update(status=Post.POST_STATUS_CHOICES[2][0], author=request.user)
    post.message_user(request, f"{updated} постов снято с публикации.", messages.SUCCESS)
    make_unpublished.short_description = "Снять с публикации выбранные посты"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author__username', 'status', 'unmodified_since', 'created_at', 'updated_at', 'views']
    list_display_links = ["id", "title"]
    list_editable = ["status"]

    search_fields = ["author__username", "title", "content", "tags__name"]

    ordering = ["-created_at"]

    actions = [make_published, make_unpublished]

    readonly_fields = ["id", "author", "views", "created_at", "updated_at", "unmodified_since"]

    @admin.display(description="Last modified")
    def unmodified_since (self, post: Post):
        if post.created_at == post.updated_at:
            return "Un modified"
        return (post.updated_at - post.created_at).total_seconds()

    inlines = [CommentInline]

    fieldsets = (
        ('Основная информация', { # Первый филдсет
            'fields': ('title', 'status')
            }),
        ('Содержимое поста', { # Второй филдсет
            'fields': ('content', 'tags', 'category'),
            'classes': ('collapse',), # Сделать блок сворачиваемым
            'description': 'Основной текст и теги для поста.'
            }),
        ('Даты (Авто)', { # Третий филдсет
            'fields': ('created_at', 'updated_at', 'unmodified_since'),
            'classes': ('collapse',)
            }),
        )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'author', 'content', 'created_at']
    list_display_links = ["id", "content"]

    search_fields = ["author__username", "title", "content"]

    ordering = ["-created_at"]

    readonly_fields = ["id", "author", "post", "content", "created_at", "updated_at", "unmodified_since"]

    @admin.display(description="Last modified")
    def unmodified_since (self, comment: Comment):
        if comment.created_at == comment.updated_at:
            return "Un modified"
        return (comment.updated_at - comment.created_at).total_seconds()

    fieldsets = (
        ('Основная информация', { # Первый филдсет
            'fields': ('content', 'author',)
            }),
        ('Содержимое поста', { # Второй филдсет
            'fields': ('post',),
            'classes': ('collapse',), # Сделать блок сворачиваемым
            'description': 'Основной текст и теги для поста.'
            }),
        ('Даты (Авто)', { # Третий филдсет
            'fields': ('created_at', 'updated_at', 'unmodified_since'),
            'classes': ('collapse',)
            }),
        )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
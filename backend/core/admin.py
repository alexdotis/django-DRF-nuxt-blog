from django.contrib import admin
from .models import Article, Comments, VoteSystem


class ArticleAdminModel(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author',
                    'article_status', 'status')
    list_editable = ('article_status',)
    search_fields = ('author__username', 'title', 'status',)
    list_filter = ('author', 'title', 'status', 'article_status',)


class CommentsAdminModel(admin.ModelAdmin):
    list_display = ('comment_text', 'user', 'article', 'comment_created_at')
    search_fields = ('user__username', 'comment_text')


class VoteSystemAdminModel(admin.ModelAdmin):
    list_display = ('content_type', 'user', 'vote', 'object_id')
    list_filter = ('user__username', 'content_type', 'object_id')


admin.site.register(Article, ArticleAdminModel)
admin.site.register(Comments, CommentsAdminModel)
admin.site.register(VoteSystem, VoteSystemAdminModel)

from os import remove
from .models import Article, Comments, VoteSystem
from rest_framework import serializers


class ArticleListSerializer(serializers.ModelSerializer):

    author = serializers.CharField()
    total_comments = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    total_dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'pk',
            'author',
            'title',
            'subheading',
            'slug',
            'created_at',
            'timestamp',
            'total_comments',
            'total_likes',
            'total_dislikes'
        )

    def get_total_comments(self, obj):
        total = Comments.objects.filter(article__title=obj).count()
        return total

    def article_queryset(self, obj):
        return Article.objects.get(title=obj)

    def get_total_likes(self, obj):
        likes = self.article_queryset(obj)
        return likes.votes.likes().count()

    def get_total_dislikes(self, obj):
        dislikes = self.article_queryset(obj)
        return dislikes.votes.dislikes().count()


class CommentArticleSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    total_likes = serializers.SerializerMethodField()
    total_dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = (
            'id',
            'user',
            'comment_text',
            'comment_created_at',
            'comment_status',
            'total_likes',
            'total_dislikes'
        )

    def comment_queryset(self, obj):
        return Comments.objects.get(id=obj.id)

    def get_total_likes(self, obj):
        likes = self.comment_queryset(obj)
        return likes.votes.likes().count()

    def get_total_dislikes(self, obj):
        dislikes = self.comment_queryset(obj)
        return dislikes.votes.dislikes().count()


SEARCH_PATTERN = '/media/uploads/'
SITE_DOMAIN = "http://127.0.0.1:8000"
REPLACE_WITH = '%s/media/uploads/' % SITE_DOMAIN


class FixAbsolutePathSerializer(serializers.Field):

    def to_representation(self, value):
        if SITE_DOMAIN in value:
            return value
        # text = value.replace('/media/uploads/','http://127.0.0.1:8000/media/uploads/')
        text = value.replace(SEARCH_PATTERN, REPLACE_WITH)
        return text


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    comments = CommentArticleSerializer(source='comments_article', many=True)
    total_comments = serializers.SerializerMethodField(
        source='comments_article')
    total_likes = serializers.SerializerMethodField()
    total_dislikes = serializers.SerializerMethodField()
    text = FixAbsolutePathSerializer()

    class Meta:
        model = Article
        fields = (
            'pk',
            'author',
            'title',
            'text',
            'subheading',
            'image',
            'created_at',
            'comments',
            'total_comments',
            'total_likes',
            'total_dislikes'
        )

    def get_total_comments(self, obj):
        return Comments.objects.filter(article__title=obj).count()

    def article_queryset(self, obj):
        return Article.objects.get(title=obj)

    def get_total_likes(self, obj):
        likes = self.article_queryset(obj)
        return likes.votes.likes().count()

    def get_total_dislikes(self, obj):
        dislikes = self.article_queryset(obj)
        return dislikes.votes.dislikes().count()


class ArticleCreateSerializer(serializers.ModelSerializer):
    author = serializers.CharField(default='author', read_only=True)

    class Meta:
        model = Article
        fields = (
            'author',
            'title',
            'subheading',
            'text',
            'image'
        )

    def validate_title(self, value):
        get_title = Article.objects.filter(title=value)
        if get_title.exists():
            raise serializers.ValidationError('title exists')
        return value


class ArticleUpdateSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    image = serializers.FileField(required=False)

    class Meta:
        model = Article
        fields = (
            'author',
            'title',
            'text',
            'subheading',
            'image'
        )
        read_only_fields = ('author', 'created_at',)


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(default='user', read_only=True)

    class Meta:
        model = Comments
        fields = ('article', 'user', 'comment_text')
        read_only_fields = ('article',)


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('comment_text', 'user',
                            'comment_status', 'article')


class GetVoteSystemSerializer(serializers.ModelSerializer):

    user = serializers.CharField(default='user')
    content_type = serializers.CharField(default='content_type')
    vote = serializers.SerializerMethodField()

    class Meta:
        model = VoteSystem
        fields = ('user', 'content_type',
                  'vote', 'object_id')

    def get_vote(self, obj):
        return obj.get_vote_display()

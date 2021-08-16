from core.models import VoteSystem
from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticleCreateView,
    CommentCreateView,
    DeleteCommentView,
    VoteSystemView,
    MyImageUploadView,
    ApiVoteSystemView,
)

from .models import Article, Comments
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('api/articles/', ArticleListView.as_view()),
    path('api/article/create/', ArticleCreateView.as_view()),
    path('api/article/<slug>/', ArticleDetailView.as_view()),
    path('api/article/<slug>/update/', ArticleUpdateView.as_view()),
    path('api/article/<slug>/delete/', ArticleDeleteView.as_view()),
    path('api/comment/<slug>/create/', CommentCreateView.as_view()),
    path('api/comment/<pk>/delete/', DeleteCommentView.as_view()),
    path('api/article/<pk>/like',
         VoteSystemView.as_view(model=Article, vote_type=VoteSystem.LIKE)),
    path('api/article/<pk>/dislike',
         VoteSystemView.as_view(model=Article, vote_type=VoteSystem.DISLIKE)),
    path('api/comment/<pk>/like',
         VoteSystemView.as_view(model=Comments, vote_type=VoteSystem.LIKE)),
    path('api/comment/<pk>/dislike',
         VoteSystemView.as_view(model=Comments, vote_type=VoteSystem.DISLIKE)),
    path('api/image/upload/', csrf_exempt(MyImageUploadView.as_view())),
    path('api/vt/', ApiVoteSystemView.as_view())

]

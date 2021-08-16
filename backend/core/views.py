from django.core.exceptions import PermissionDenied
from rest_framework import generics, mixins
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    ArticleDetailSerializer,
    ArticleUpdateSerializer,
    ArticleCreateSerializer,
    CommentCreateSerializer,
    CommentDetailSerializer,
    ArticleListSerializer,
    GetVoteSystemSerializer
)

from .models import Article, Comments, VoteSystem
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils.html import escape
from django.views import generic
from ckeditor_uploader.backends import registry
from ckeditor_uploader.utils import storage
from ckeditor_uploader.views import get_upload_filename
from ckeditor_uploader import utils
import os


class MyImageUploadView(generic.View):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, **kwargs):
        """
        Uploads a file and send back its URL to CKEditor.
        """
        uploaded_file = request.FILES["upload"]

        backend = registry.get_backend()

        ck_func_num = request.GET.get("CKEditorFuncNum")
        if ck_func_num:
            ck_func_num = escape(ck_func_num)

        filewrapper = backend(storage, uploaded_file)
        allow_nonimages = getattr(
            settings, "CKEDITOR_ALLOW_NONIMAGE_FILES", True)
        # Throws an error when an non-image file are uploaded.
        if not filewrapper.is_image and not allow_nonimages:
            return HttpResponse(
                """
                <script type='text/javascript'>
                window.parent.CKEDITOR.tools.callFunction({0}, '', 'Invalid file type.');
                </script>""".format(
                    ck_func_num
                )
            )

        filepath = get_upload_filename(uploaded_file.name, request)

        saved_path = filewrapper.save_as(filepath)

        url = utils.get_media_url(saved_path)

        if ck_func_num:
            # Respond with Javascript sending ckeditor upload url.
            return HttpResponse(
                """
            <script type='text/javascript'>
                window.parent.CKEDITOR.tools.callFunction({0}, '{1}');
            </script>""".format(
                    ck_func_num, url
                )
            )
        else:
            SITE_NAME = 'http://127.0.0.1:8000'
            _, filename = os.path.split(saved_path)
            retdata = {"url": SITE_NAME + url,
                       "uploaded": "1", "fileName": filename}
            return JsonResponse(retdata)


class CustomPagination(PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    model = Article
    queryset = Article.objects.filter(status=True)
    pagination_class = CustomPagination


class ArticleDetailView(generics.RetrieveAPIView):
    lookup_field = 'slug'
    model = Article
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer


class ArticleCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    model = Article
    serializer_class = ArticleCreateSerializer
    queryset = Article.objects.all()

    def perform_create(self, serializer):

        serializer.save(author=self.request.user)


class ArticleUpdateView(generics.RetrieveAPIView, mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    model = Article
    queryset = Article.objects.all()
    serializer_class = ArticleUpdateSerializer

    def put(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if user.is_staff or user.is_superuser:
            return self.update(request, *args, **kwargs)

        if not str(instance.author) == user.username:
            raise PermissionDenied

        return self.update(request, *args, **kwargs)


class ArticleDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'
    model = Article
    queryset = Article.objects.all()

    def delete(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if user.is_staff or user.is_superuser:
            return self.destroy(request, *args, **kwargs)
        if not str(instance.author) == user.username:
            raise PermissionDenied
        return self.destroy(request, *args, **kwargs)


# Comments

class CommentCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    model = Comments
    serializer_class = CommentCreateSerializer
    queryset = Comments.objects.all()

    def get_article_id(self):
        slug = self.kwargs['slug']
        article = Article.objects.filter(slug=slug)
        if not article.exists():
            raise Http404
        return article.first().id

    def post(self, request, *args, **kwargs):
        article_id = self.get_article_id()

        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, article_id=article_id)
        return Response({'detail': 'success'})


class DeleteCommentView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    model = Comments
    serializer_class = CommentDetailSerializer
    queryset = Comments.objects.all()

    def delete(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if instance.user == user:
            return self.destroy(request, *args, **kwargs)


class VoteSystemView(APIView):
    permission_classes = (IsAuthenticated,)
    model = None
    vote_type = None

    def post(self, request, *args, **kwargs):
        obj = self.model.objects.get(pk=self.kwargs['pk'])
        try:
            likeordislike = VoteSystem.objects.get(content_type=ContentType.objects.get_for_model(
                obj), object_id=obj.id, user=request.user)

            if likeordislike.vote is not self.vote_type:
                likeordislike.vote = self.vote_type
                likeordislike.save()
                result = True
            else:
                likeordislike.delete()
                result = False
        except VoteSystem.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return Response({'details': result})


class ApiVoteSystemView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetVoteSystemSerializer
    model = VoteSystem

    def get_queryset(self):
        queryset = VoteSystem.objects.filter(
            user__username=self.request.user)
        return queryset

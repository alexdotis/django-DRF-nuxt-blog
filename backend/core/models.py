from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


def article_image_path(instance, filename):
    return f"{instance.title}/{filename}"


class Article(models.Model):
    choices = (
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Deny', 'Deny')
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=100)
    subheading = models.CharField(_("subheading"), max_length=80)
    text = RichTextUploadingField()
    created_at = models.DateField(_("created"), auto_now=True)
    timestamp = models.DateTimeField(_("timestamp"), auto_now=True)
    image = models.ImageField(_('image'), upload_to=article_image_path)

    slug = models.SlugField(_("slug"), blank=True,
                            null=True, editable=False, unique=True)

    status = models.BooleanField(_("status"), default=False)
    article_status = models.CharField(
        _("choices"), choices=choices, max_length=50, default=choices[0])

    votes = GenericRelation('VoteSystem')

    class Meta:
        verbose_name_plural = 'Articles'
        ordering = ('-timestamp',)

    def __str__(self) -> str:
        return self.title


@receiver(pre_save, sender=Article)
def prepopulate_slug(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)


@receiver(pre_save, sender=Article)
def status_check(sender, instance, *args, **kwargs):
    if instance.article_status == 'Success':
        instance.status = True
    else:
        instance.status = False


class Comments(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments_article')

    user = models.ForeignKey(
        User, on_delete=models.CASCADE)

    comment_text = models.TextField(_("comment"))
    comment_created_at = models.DateField(_("created"), auto_now=True)
    comment_status = models.BooleanField(_("status"), default=True)
    votes = GenericRelation('VoteSystem')

    class Meta:
        verbose_name_plural = 'Comments'
        ordering = ('comment_created_at',)

    def __str__(self) -> str:
        return self.comment_text


class VoteSystemManager(models.Manager):

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)


class VoteSystem(models.Model):
    LIKE = 1
    DISLIKE = -1
    vote_type = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike')
    )

    vote = models.IntegerField(_('vote'), choices=vote_type)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = VoteSystemManager()

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

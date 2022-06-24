from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Blog(models.Model):
    """Blog model using 'tinymce' text editors with 'comment' and 'files' as GenericRelation"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_('author'),
                               on_delete=models.CASCADE,
                               related_name='blog_author')
    title = models.CharField(verbose_name=_('title'), max_length=200)
    # content = RichTextField(verbose_name=_('content'))
    content = RichTextUploadingField(verbose_name=_('content'))
    likes = models.PositiveIntegerField(verbose_name=_('likes'), default=0)
    is_published = models.BooleanField(verbose_name=_('is published'), default=True)
    publish_date = models.DateTimeField(verbose_name=_('publish date'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('updated'), auto_now=True)
    slug = models.SlugField(blank=True)
    comments = GenericRelation('Comment')
    files = GenericRelation('File')

    class Meta:
        # DB index used for better speed
        # https://docs.djangoproject.com/en/4.0/ref/models/options/#indexes
        ordering = ['-publish_date', 'title']
        indexes = [
            models.Index(fields=['author', 'title', '-publish_date']),
            models.Index(fields=['content'], name='content_index'),
        ]

    def __str__(self):
        return f'{self.title} by {self.author}'
    
    # To slugify datetime object (and hence convert it to str format) we used these documents:
    # https://docs.python.org/3/library/datetime.html#datetime.datetime.strftime
    # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.title}')
        if self.updated:
            self.slug = slugify(f'{self.title}_{self.updated.strftime("%Y-%m-%d---%H-%M")}')
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_('user'),
                             on_delete=models.SET_NULL,
                             related_name='comment_user',
                             blank=True,
                             null=True)
    content = models.TextField(verbose_name=_('content'), blank=True, null=True)
    like = models.PositiveIntegerField(verbose_name=_('like'), default=0)
    dislike = models.PositiveIntegerField(verbose_name=_('dislike'), default=0)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('updated'), auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self) -> str:
        if self.user:
            return f'comment {self.id} by {self.user.name}'


class File(models.Model):
    file = models.FileField(verbose_name=_('file'))
    describe = models.CharField(verbose_name=_('describe'), max_length=100, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

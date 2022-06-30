from django.db import models
from django.conf import settings

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    body = RichTextField(blank=True, features=settings.WAGTAIL_EDITOR_FEAUTURES)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

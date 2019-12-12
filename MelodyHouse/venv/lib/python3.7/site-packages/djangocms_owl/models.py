# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.db import models
from django.utils.translation import ugettext as _

from cms.models import CMSPlugin
from jsonfield import JSONField

from .conf import settings


class AbstractOwlBase(CMSPlugin):
    extra_options = JSONField(_('JSON options'), blank=True)

    class Meta:
        abstract = True


class OwlCarousel(AbstractOwlBase):
    pagination = models.BooleanField(
        default=False,
        help_text=_('Show pagination. (dot dot dot)'), )
    pagination_numbers = models.BooleanField(
        default=False,
        help_text=_('Show numbers inside pagination buttons'), )
    navigation = models.BooleanField(
        default=False,
        help_text=_('Display "next" and "prev" buttons.'), )

    autoplay = models.BooleanField(
        default=False,
        help_text=_('Slides cycle automatically every 5 seconds'))
    stop_on_hover = models.BooleanField(
        default=False,
        help_text=_('Stop autoplay on mouse hover'), )

    items = models.PositiveSmallIntegerField(
        default=1,
        help_text=_('maximum amount of items displayed at a time'), )

    auto_height = models.BooleanField(
        default=False,
        help_text=_('Add height to owl-wrapper-outer so you can use different heights on slides.'), )

    style = models.CharField(
        _('style'),
        max_length=255,
        choices=settings.DJANGOCMS_OWL_STYLES,
        default=settings.DJANGOCMS_OWL_STYLES[0][0],
        help_text=_('CSS class'), )
    template = models.CharField(
        _('template'),
        max_length=255,
        choices=settings.DJANGOCMS_OWL_TEMPLATES,
        default=settings.DJANGOCMS_OWL_TEMPLATES[0][0], )

    def get_style(self):
        if self.style and self.style != 'default':
            return self.style
        return ''

    def get_owl_options(self):
        options = {
            'pagination': True if self.pagination else False,
            'paginationNumbers': True if self.pagination_numbers else False,
            'items': self.items,
            'navigation': True if self.navigation else False,
            'autoPlay': True if self.autoplay else False,
            'stopOnHover': True if self.stop_on_hover else False,
            'autoHeight': True if self.auto_height else False,
            'singleItem': True if self.items == 1 else False,

            # Defaults to be overriden in extra (for now)
            'itemsDesktopSmall': False,
            'itemsTablet': False,
            'itemsMobile': False,
        }

        if self.extra_options:
            options.update(self.extra_options)

        return options

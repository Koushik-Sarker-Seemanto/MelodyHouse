try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.template.loader import select_template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .conf import settings
from .models import OwlCarousel


class OwlCarouselPlugin(CMSPluginBase):
    name = _('Owl Carousel')
    module = settings.DJANGOCMS_OWL_MODULE
    model = OwlCarousel
    allow_children = True
    child_classes = settings.DJANGOCMS_OWL_CHILD_CLASSES
    render_template = 'djangocms_owl/default.html'
    fieldsets = (
        (None, {
            'fields': (
                'items',
                'auto_height',
            )
        }),
        (_('Navigation'), {
            'fields': (
                'pagination',
                'pagination_numbers',
                'navigation',

            ),
        }),
        (_('AutoPlay'), {
            'fields': (
                'autoplay',
                'stop_on_hover',
            ),
        }),
        (_('Style'), {
            'fields': (
                'style',
                'template',
            ),
        }),
        (_('Extra'), {
            'classes': ('collapse', ),
            'fields': (
                'extra_options',
            ),
        }),
    )

    def render(self, context, instance, placeholder):
        context = super(OwlCarouselPlugin, self).render(context, instance, placeholder)
        context.update({
            'INCLUDE_CSS': settings.DJANGOCMS_OWL_INCLUDE_CSS,
            'INCLUDE_JS_OWL': settings.DJANGOCMS_OWL_INCLUDE_JS_OWL,
            'INCLUDE_JS_JQUERY': settings.DJANGOCMS_OWL_INCLUDE_JS_JQUERY,
            'style': instance.get_style(),
            'options': mark_safe(json.dumps(instance.get_owl_options())),
        })
        return context

    @staticmethod
    def get_render_template(context, instance, placeholder):
        return instance.template + '.html'


plugin_pool.register_plugin(OwlCarouselPlugin)

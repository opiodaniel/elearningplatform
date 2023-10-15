# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


@apphook_pool.register  # register the application
class Core1App(CMSApp):

    app_name = 'core1'

    name = _('core1')

    def get_urls(self, page=None, language=None, **kwargs):
        return ["elearning.apps.core1.urls"]


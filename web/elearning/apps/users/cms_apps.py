# -*- coding: utf-8 -*-

# https://djangocms.readthedocs.io/en/latest/how_to/apphooks/

from __future__ import unicode_literals
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


@apphook_pool.register  # register the application
class UsersApp(CMSApp):

    app_name = 'users'  # If you want to attach an application multiple times to different pages, then the class defining the apphook must have an app_name attribute:

    name = _('Users')  # s a human-readable name for the admin user.

    def get_urls(self, page=None, language=None, **kwargs):
        return ["elearning.apps.users.urls"]


"""elearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# apphook
#  An  apphook allows you to attach a Django application to a page. For example, you might have a news application that you’d like integrated with django CMS. In this case, you can create a normal django CMS page without any content of its own, and attach the news application to the page; the news application’s content will be delivered at the page’s URL.
#  All URLs in that URL path will be passed to the attached application’s URL configs.
from cms.sitemaps import CMSSitemap
from django.contrib.sitemaps.views import sitemap

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(r'sitemap\.xml', sitemap, {'sitemaps': {'cmspages': CMSSitemap}}),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path(r'core1/', include('elearning.apps.core1.urls')),
    path(r'core/', include('elearning.apps.core.urls')),
    path(r'actions/', include('elearning.apps.actions.urls')),
    path(r'research/', include('elearning.apps.research.urls')),
    path(r'allauth/', include('allauth.urls')),
    path(r'', include('cms.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


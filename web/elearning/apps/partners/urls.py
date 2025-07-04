from django.urls import path
from django.conf.urls import url
from .views import (home, contact_us, partner_detail, instructors, instructor_tag, course_description, program_description,
                    category_description, service_description, event_description)

app_name = "partners"

# note use url when dealing with (?P<pk>\d+)
urlpatterns = [
    path('', home, name='home'),
    path('contact_us', contact_us, name='contact_us'),
    url(r'^course_description/(?P<pk>\d+)/$', course_description, name='course_description'),
    url(r'^program_description/(?P<pk>\d+)/$', program_description, name='program_description'),
    url(r'^service_description/(?P<pk>\d+)/$', service_description, name='service_description'),
    url(r'^category_description/(?P<pk>\d+)/$', category_description, name='category_description'),
    url(r'^event_description/(?P<pk>\d+)/$', event_description, name='event_description'),
    path('instructors/', instructors, name='instructors'),
    path('partner_detail/<slug:slug>/', partner_detail, name='partner_detail'),
]


from django.shortcuts import render
from .models import Partners, Instructors
from taggit.models import Tag
from django.shortcuts import get_object_or_404
from django.conf import settings
from redis import StrictRedis
from .models import Course, Program, PersonsPhrase, Category, Event, WhyUS, Services, InstitutionWeb
from ..courses.models import CourseSchedule, CourseScheduleUser
from django.contrib.auth.models import User
# from allauth.account.forms import LoginForm, SignupForm
from django.contrib.sites.shortcuts import get_current_site
from ..core.utils import log_debug
from .models import ReceivedMessages
from django.core.mail import EmailMessage
from django.http import JsonResponse

try:
    r = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
except Exception:
    print("redis try failed")

from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    print('partners home0: ')
    courses = Course.objects.all()
    programs = Program.objects.all()
    services = Services.objects.all()
    persons_phrase = PersonsPhrase.objects.all()
    categories = Category.objects.all()
    events = Event.objects.all()
    why_us_ = WhyUS.objects.all()
    institution = InstitutionWeb.objects.get(id=1)
    return render(request, 'partners/home.html', {
                                                  'courses': courses,
                                                  'programs': programs,
                                                  'services': services,
                                                  'persons_phrase_': persons_phrase,
                                                  'categories': categories,
                                                  'events': events,
                                                  'why_us': why_us_,
                                                  'institution': institution,
                                                  }
                  )


def instructors(request, slug=None):
    instructors_ = Instructors.objects.all().order_by('order')
    if slug:
        instructor_ = Instructors.objects.get(slug=slug)
    else:
        instructor_ = Instructors.objects.all().order_by('order')[0]
    return render(request, 'partners/instructors.html', {
        'instructors': instructors_,
        'instructor': instructor_
    })


def instructor_tag(request, slug=None):
    instructors_ = Instructors.objects.all().order_by('order')
    tag = None
    if slug:
        try:
            tag = get_object_or_404(Tag, slug=slug)
            instructors_ = instructors_.filter(tags__in=[tag])
        except Exception as er:
            print(er)
    instructor_ = Instructors.objects.all().order_by('order')[0]
    return render(request, 'partners/instructors.html', {
        'instructors': instructors_,
        'instructor': instructor_,
        'tag': tag
    })


def partner_detail(request, slug):
    partner = Partners.objects.get(slug=slug)
    return render(request, 'partners/partner.html', {'partner': partner})


def course_description(request, pk):
    institution = InstitutionWeb.objects.get(id=1)
    course = Course.objects.get(id=pk)
    return render(request, 'partners/descriptions/course_description.html',
                  {'course': course,
                   'institution_obj': institution,
                   })


def program_description(request, pk):
    institution = InstitutionWeb.objects.get(id=1)
    program = Program.objects.get(id=pk)
    return render(request, 'partners/descriptions/program_description.html',
                  {'program': program,
                   'institution_obj': institution,
                   })


def service_description(request, pk):
    institution = InstitutionWeb.objects.get(id=1)
    service = Services.objects.get(id=pk)
    return render(request, 'partners/descriptions/service_description.html',
                  {'service': service,
                   'institution_obj': institution,
                   })


def category_description(request, pk):
    institution = InstitutionWeb.objects.get(id=1)
    category = Category.objects.get(id=pk)
    return render(request, 'partners/descriptions/category_description.html',
                  {'category': category,
                   'institution_obj': institution,
                   })


def event_description(request, pk):
    institution = InstitutionWeb.objects.get(id=1)
    event = Event.objects.get(id=pk)
    return render(request, 'partners/descriptions/event_description.html',
                  {'event': event,
                   'institution_obj': institution,
                   })


def contact_us(request):
    company_obj = InstitutionWeb.objects.get(id=1)
    if request.method == 'POST':
        contact_us_name_ = request.POST.get('name')
        contact_us_name = contact_us_name_.upper()
        contact_us_email = request.POST.get('email')
        contact_us_subject = request.POST.get('subject')
        contact_us_message = request.POST.get('message')
        print(121222222222222222222222222222)
        if contact_us_subject == '' or contact_us_message == '':
            rr = {'status': 'Must enter subject and a message!'}
        else:
            try:
                ReceivedMessages.objects.create(institution_web=company_obj,
                                                name=contact_us_name,
                                                email=contact_us_email,
                                                subject=contact_us_subject,
                                                message=contact_us_message)
                contact_us_message = 'Message received from ' + contact_us_name + ' \nEmail:' + contact_us_email + ' \nMessage:\n' + contact_us_message
                print(22222222222222222222222)
                email = EmailMessage(contact_us_subject, contact_us_message, contact_us_email, [company_obj.email])
                print(contact_us_message)
                email.send()
                print(contact_us_email)
                print(company_obj.email)
                rr = {'status': " "+contact_us_name+" "+'Your message was received.\n\nThank you.'}
            except Exception as ee:
                print(ee)
                return_message = 'Error in sending your message.\n\nPlease try again.'
                rr = {'status': 'ko', 'return_message':return_message}
    return JsonResponse(rr)
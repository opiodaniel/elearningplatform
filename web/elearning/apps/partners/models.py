from django.db import models
from django.conf import settings
from ..core.fields import OrderField
from ..users.models import Institution
from cms.models.fields import PlaceholderField
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.utils.translation import ugettext_lazy as _
from ..courses.models import Course
from ..courses.models import CourseScheduleUser

class Partners(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='partners')
    order = OrderField(blank=True, for_fields=[], default=1)
    organization_name = models.CharField(max_length=128, default='')
    address1 = models.CharField(max_length=128, blank=True, null=True)
    address2 = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField()
    city = models.CharField(max_length=128, default='')
    country = models.CharField(max_length=128, default='')
    office_phone = models.CharField(max_length=128, default='')
    cell_phone = models.CharField(max_length=128, default='')
    owner_image = models.ImageField(upload_to='partners/%Y/%m/%d/', blank=True, null=True)
    organization_image = models.ImageField(upload_to='partners/%Y/%m/%d/', blank=True, null=True)
    description = PlaceholderField('partner_description')
    slug = models.SlugField(max_length=250, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.owner.get_full_name() + '-' + self.id)
        super(Partners, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('partners:partner_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.owner.get_full_name()


class Instructors(models.Model):
    class Meta:
        ordering = ['order']
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructors')
    order = models.IntegerField(blank=True, default=10000)
    institution = models.ManyToManyField(Institution, blank=True, related_name="institution_instructors")
    short_bio = PlaceholderField('partner_short_bio', related_name="short_bio")
    full_bio = PlaceholderField('partner_full_bio', related_name="full_bio")
    tags = TaggableManager()
    slug = models.SlugField(max_length=250, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.get_full_name() + '-' + self.id)
        super(Instructors, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('instructors:instructor', kwargs={'slug': self.slug})

    def __str__(self):
        return self.user.get_full_name()


class Publications(models.Model):
    class Meta:
        ordering = ['-year', 'order']

    instructor = models.ForeignKey(Instructors, on_delete=models.CASCADE,
                                   related_name='publications')
    order = OrderField(blank=True, for_fields=[], default=1)
    title = models.CharField(max_length=128, default='')
    publisher = models.CharField(max_length=128, default='')
    year = models.SmallIntegerField(default='2020')
    citation = models.CharField(max_length=256, default='')

    def __str__(self):
        return self.citation


# ============ Home page ===========


class InstitutionWeb(models.Model):

    class Meta:
        verbose_name = _('institution')
        verbose_name_plural = _('institutions')
        ordering = ['order']

    order = models.IntegerField(default=1000, null=True, blank=True)
    institution_name = models.CharField(max_length=100, null=True, blank=True)
    welcome_phrase_title = models.CharField(max_length=200, null=True, blank=True)
    welcome_phrase_title_description = models.CharField(max_length=1000, null=True, blank=True)
    institution_image = models.ImageField(upload_to='institution/', blank=True, null=True)
    institution_motion_image = models.ImageField(upload_to='institution/', blank=True, null=True)
    institution_logo_image = models.ImageField(upload_to='institution/', blank=True, null=True)
    join_us_title = models.CharField(max_length=100, default='', null=True, blank=True)

    course_header = models.CharField(max_length=100, null=True, blank=True)
    course_description_one = models.CharField(max_length=1000, null=True, blank=True)
    course_description_two = models.CharField(max_length=1000, null=True, blank=True)

    category_header = models.CharField(max_length=100, null=True, blank=True)
    category_description_one = models.CharField(max_length=1000, null=True, blank=True)
    category_description_two = models.CharField(max_length=1000, null=True, blank=True)

    event_header = models.CharField(max_length=100, null=True, blank=True)
    event_description_one = models.CharField(max_length=1000, null=True, blank=True)
    event_description_two = models.CharField(max_length=1000, null=True, blank=True)

    section_two_header = models.CharField(max_length=100, null=True, blank=True)
    section_two_description_one = models.CharField(max_length=1000, null=True, blank=True)
    section_two_description_two = models.CharField(max_length=1000, null=True, blank=True)
    section_two_image = models.ImageField(upload_to='institution/', blank=True, null=True)
    section_two_motion_image = models.ImageField(upload_to='institution/', blank=True, null=True)

    section_three_header = models.CharField(max_length=100, null=True, blank=True)
    section_three_description_one = models.CharField(max_length=1000, null=True, blank=True)
    section_three_description_two = models.CharField(max_length=1000, null=True, blank=True)
    section_three_image = models.ImageField(upload_to='institution/', blank=True, null=True)

    def __str__(self):
        return self.institution_name


class Course(models.Model):

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE, default=1, related_name='courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=21, related_name='course_courses')
    order = models.IntegerField(default=1000, blank=True)
    fee = models.CharField(max_length=30, default='0', null=True)
    course_name = models.CharField(max_length=100, null=True)
    number_of_registered_students_for_the_course = models.IntegerField(default=0, blank=True)
    course_image = models.ImageField(upload_to='courses/', blank=True, null=True)
    is_popular = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_links = models.BooleanField(default=True)
    description = PlaceholderField('description', related_name='education_course_description')


class Program(models.Model):

    class Meta:
        verbose_name = _('Program')
        verbose_name_plural = _('Programs')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE,  default=1, related_name='programs')
    order = models.IntegerField(default=1000, blank=True)
    program_image = models.ImageField(upload_to='Programs/', blank=True, null=True)
    program_name = models.CharField(max_length=100, null=True)
    program_description = models.CharField(max_length=500, null=True)
    program_link_title = models.CharField(max_length=500, null=True)
    is_popular = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_links = models.BooleanField(default=True)
    description = PlaceholderField('description', related_name='program_description')


class PersonsPhrase(models.Model):

    class Meta:
        verbose_name = _('phrase')
        verbose_name_plural = _('phrases')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE, default=1, related_name='phrases')
    order = models.IntegerField(default=1000, blank=True)
    persons_phrase_image = models.ImageField(upload_to='phrase/', blank=True, null=True)
    persons_phrase = models.CharField(max_length=500, null=True)
    persons_name = models.CharField(max_length=500, null=True)
    persons_job_title = models.CharField(max_length=500, null=True)
    is_active = models.BooleanField(default=True)
    is_links = models.BooleanField(default=True)


class Category(models.Model):

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE, default=1, related_name='categories')
    order = models.IntegerField(default=1000, blank=True)
    category_image = models.ImageField(upload_to='category/', blank=True, null=True)
    category_name = models.CharField(max_length=50, blank=True, null=True)
    number_of_courses = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_links = models.BooleanField(default=True)
    description = PlaceholderField('description', related_name='category_description')


class Event(models.Model):

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE, default=1, related_name='events')
    order = models.IntegerField(default=1000, blank=True)
    event_image = models.ImageField(upload_to='event/', blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    event_name = models.CharField(max_length=50, blank=True, null=True)
    event_location = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_links = models.BooleanField(default=True)
    description = PlaceholderField('description', related_name='event_description')


class WhyUS(models.Model):

    class Meta:
        verbose_name = _('whyus')
        verbose_name_plural = _('whyuses')
        ordering = ['order']

    institution_web = models.ForeignKey(InstitutionWeb, on_delete=models.CASCADE, default=1, related_name='whyuses')
    order = models.IntegerField(default=1000, blank=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    icon_name = models.CharField(max_length=50, blank=True, null=True)
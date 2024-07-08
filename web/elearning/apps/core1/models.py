from django.db import models
from cms.models.fields import PlaceholderField


class News(models.Model):

    class Meta:
        verbose_name = 'new'
        verbose_name_plural = 'news'
        ordering = ['id']
    topic_name = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='phrase/', blank=True, null=True)
    description = PlaceholderField('description', related_name='topic_description')
# Create your models here.

# Generated by Django 3.2 on 2023-09-24 10:08

import cms.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(blank=True, max_length=50, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='phrase/')),
                ('description', cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topic_description', slotname='description', to='cms.placeholder')),
            ],
            options={
                'verbose_name': 'new',
                'verbose_name_plural': 'news',
                'ordering': ['id'],
            },
        ),
    ]

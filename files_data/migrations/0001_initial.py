# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-28 22:48
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalEmployee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=400, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('job_title', models.TextField(blank=True, null=True)),
                ('job_title_prev', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, null=True), size=None)),
                ('company_id', models.IntegerField(blank=True, null=True)),
                ('capacity_rate', models.FloatField(blank=True, null=True)),
                ('location', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('location_prev', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('skills', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('ai_endorsements', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), size=None)),
                ('experience', models.IntegerField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('ai_job_started', models.CharField(blank=True, max_length=500, null=True)),
                ('ai_current_working_started', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('ai_previous_working_started', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('ai_previous_working_finished', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('ai_current_job_title', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None)),
                ('ai_previous_job_title', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None)),
                ('ai_current_company', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('ai_previous_company', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('ai_current_locations', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('ai_previoius_locations', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('ai_current_working_content', models.TextField(blank=True, null=True)),
                ('ai_previous_working_content', models.TextField(blank=True, null=True)),
                ('ai_company', models.CharField(blank=True, max_length=500, null=True)),
                ('ai_interests_current_related', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('ai_interests', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('ai_education', models.CharField(blank=True, max_length=500, null=True)),
                ('ai_previous_education', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('ai_degree', models.CharField(blank=True, max_length=500, null=True)),
                ('ai_previous_degree', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('ai_education_field', models.CharField(blank=True, max_length=500, null=True)),
                ('ai_previous_education_field', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('ai_education_start', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('ai_education_finished', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('ai_self_intro', models.TextField(blank=True, null=True)),
                ('ai_volunteer_experience', models.TextField(blank=True, null=True)),
                ('recommendation_given', models.TextField(blank=True, null=True)),
                ('recommendation_received', models.TextField(blank=True, null=True)),
                ('ai_activity_articles', models.TextField(blank=True, null=True)),
                ('ai_activity_posts', models.TextField(blank=True, null=True)),
                ('ai_activity_liked', models.TextField(blank=True, null=True)),
                ('activity_followers', models.IntegerField(blank=True, null=True)),
                ('accomplishment_language', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('accomplishment_course', models.TextField(blank=True, null=True)),
                ('accomplishment_project', models.TextField(blank=True, null=True)),
                ('accomplishment_certification', models.TextField(blank=True, null=True)),
                ('accomplishment_organization', models.TextField(blank=True, null=True)),
                ('accomplishment_honor', models.TextField(blank=True, null=True)),
                ('accomplishment_publication', models.TextField(blank=True, null=True)),
                ('accomplishment_patent', models.TextField(blank=True, null=True)),
                ('accomplishment_scorer', models.TextField(blank=True, null=True)),
                ('is_active', models.CharField(blank=True, max_length=500, null=True)),
                ('currrent_position', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('current_company', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('most_important_certificate', models.CharField(blank=True, max_length=500, null=True)),
                ('most_important_education', models.CharField(blank=True, max_length=500, null=True)),
                ('facebook_link', models.CharField(blank=True, max_length=500, null=True)),
                ('twitter_link', models.CharField(blank=True, max_length=500, null=True)),
                ('emails', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('all_links', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
            ],
        ),
    ]

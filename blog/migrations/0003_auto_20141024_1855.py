# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random

from django.db import models, migrations


def create_more_data(apps, schema_editor):
    Author = apps.get_model('blog', 'Author')
    authors = list(Author.objects.all())

    Tag = apps.get_model('blog', 'Tag')
    tags = list(Tag.objects.all())

    # Create 1000 posts with a random author and random tag chosen
    Post = apps.get_model('blog', 'Post')

    for i in range(1000):
        post_one = Post.objects.create(body='Blog post text for random post {}'.format(i),
                                            title='Post #{}'.format(i),
                                            author=random.choice(authors))
        post_one.tags.add(random.choice(tags), random.choice(tags))


def dumb_function(schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20141018_2245'),
    ]

    operations = [
        migrations.RunPython(create_more_data, reverse_code=dumb_function)
    ]

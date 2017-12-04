# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('automated_survey', '0004_auto_20150827_2118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='kind',
        ),
    ]

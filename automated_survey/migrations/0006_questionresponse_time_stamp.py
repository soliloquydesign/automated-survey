# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('automated_survey', '0005_remove_question_kind'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionresponse',
            name='time_stamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 12, 6, 5, 10, 14, 767527, tzinfo=utc)),
            preserve_default=False,
        ),
    ]

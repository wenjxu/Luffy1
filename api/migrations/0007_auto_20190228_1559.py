# Generated by Django 2.0.7 on 2019-02-28 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20190228_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesection',
            name='order',
            field=models.SmallIntegerField(help_text='建议每个课时之间空1至2个值，以备后续插入课时', verbose_name='课时排序'),
        ),
    ]
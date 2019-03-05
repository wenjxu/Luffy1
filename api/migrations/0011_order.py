# Generated by Django 2.0.7 on 2019-03-04 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20190228_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('order_num', models.CharField(max_length=32)),
                ('status', models.IntegerField(choices=[(1, '未支付'), (2, '已支付')], default=1)),
            ],
            options={
                'verbose_name_plural': '16.支付',
            },
        ),
    ]

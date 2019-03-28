# Generated by Django 2.1.5 on 2019-03-28 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawsuits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawsuit',
            name='area',
            field=models.CharField(default=None, max_length=128, verbose_name='法院名'),
        ),
        migrations.AddField(
            model_name='lawsuit',
            name='crime_type_detail',
            field=models.CharField(default=None, max_length=128, verbose_name='案由'),
        ),
        migrations.AddField(
            model_name='lawsuit',
            name='date',
            field=models.DateTimeField(default=None, verbose_name='判决日期'),
        ),
        migrations.AddField(
            model_name='lawsuit',
            name='defendant',
            field=models.CharField(default=None, max_length=256, verbose_name='被告'),
        ),
        migrations.AddField(
            model_name='lawsuit',
            name='people_at_party',
            field=models.CharField(default=None, max_length=256, verbose_name='当事人描述'),
        ),
        migrations.AddField(
            model_name='lawsuit',
            name='plaintiff',
            field=models.CharField(default=None, max_length=256, verbose_name='原告'),
        ),
        migrations.AddField(
            model_name='lawsuit',
            name='proc_type',
            field=models.CharField(choices=[(0, '判决书'), (1, '裁定书')], default=1, max_length=16, verbose_name='文书类型'),
        ),
        migrations.AddField(
            model_name='lawsuit',
            name='procedure',
            field=models.CharField(choices=[(0, '一审'), (1, '二审'), (2, '其他')], default=0, max_length=16, verbose_name='庭审程序'),
        ),
        migrations.AddField(
            model_name='lawsuit',
            name='third_party',
            field=models.CharField(default=None, max_length=256, verbose_name='第三人'),
        ),
        migrations.AlterField(
            model_name='lawsuit',
            name='crime_type',
            field=models.CharField(choices=[(0, '民事'), (1, '刑事')], max_length=16, verbose_name='案件类型'),
        ),
    ]

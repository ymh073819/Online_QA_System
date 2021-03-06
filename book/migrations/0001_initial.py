# Generated by Django 2.0 on 2018-01-06 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('author', models.CharField(max_length=10)),
                ('content', models.TextField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('student_number', models.CharField(blank=True, max_length=50, null=True)),
                ('telephone', models.CharField(max_length=20, null=True)),
                ('email', models.CharField(max_length=30, null=True)),
                ('QQ', models.CharField(max_length=20, null=True)),
                ('address', models.CharField(max_length=50, null=True)),
                ('birthday', models.CharField(max_length=10, null=True)),
            ],
        ),
    ]

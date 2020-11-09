# Generated by Django 3.1.3 on 2020-11-07 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('pages', models.CharField(max_length=5)),
                ('image', models.ImageField(default='default.jpg', upload_to='book_pics')),
                ('is_available', models.BooleanField()),
            ],
        ),
    ]

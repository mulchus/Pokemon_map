# Generated by Django 4.1.7 on 2023-03-10 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0024_alter_pokemonentity_pokemon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='изображение'),
        ),
    ]
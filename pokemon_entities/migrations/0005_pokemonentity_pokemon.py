# Generated by Django 4.1.7 on 2023-02-25 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0004_pokemonentity'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.pokemon'),
            preserve_default=False,
        ),
    ]
# Generated by Django 4.1.7 on 2023-03-10 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0023_alter_pokemon_previous_evolution_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entities', to='pokemon_entities.pokemon', verbose_name='название покемона'),
        ),
    ]

from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(verbose_name='название', max_length=200)
    title_en = models.CharField(verbose_name='название по английский', max_length=200, blank=True)
    title_jp = models.CharField(verbose_name='название по японски', max_length=200, blank=True)
    photo = models.ImageField(verbose_name='изображение', null=True, blank=True)
    description = models.TextField(verbose_name='описание', blank=True)
    previous_evolution = models.ForeignKey('self', verbose_name='из кого эволюционировал',
                                           related_name='next_evolutions',
                                           on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, verbose_name='название покемона',
                                related_name='entities', on_delete=models.SET_NULL, null=True)
    lat = models.FloatField(verbose_name='широта', null=True)
    lon = models.FloatField(verbose_name='долгота', null=True)
    appeared_at = models.DateTimeField(verbose_name='появление', null=True)
    disappeared_at = models.DateTimeField(verbose_name='исчезновение', null=True)
    level = models.IntegerField(verbose_name='уровень', null=True)
    health = models.IntegerField(verbose_name='здоровье', null=True, blank=True)
    strength = models.IntegerField(verbose_name='сила', null=True, blank=True)
    defence = models.IntegerField(verbose_name='защита', null=True, blank=True)
    stamina = models.IntegerField(verbose_name='выносливость', null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon} {self.id} {self.appeared_at}'

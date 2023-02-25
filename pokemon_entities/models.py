from django.db import models  # noqa F401


class Pokemon(models.Model):
    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    photo = models.ImageField(null=True)

    def __str__(self):
        if self.is_active:
            return self.title
        return f'{self.title} (inactive)'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)


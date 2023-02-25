from django.db import models  # noqa F401


class Pokemon(models.Model):
    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=200)

    def __str__(self):
        if self.is_active:
            return self.title
        return f'{self.title} (inactive)'

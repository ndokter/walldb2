from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    auto_generated = models.BooleanField(default=False)

    def __str__(self):
        return self.name

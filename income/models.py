from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.source} -> ${self.amount}"
    
    class Meta:
        ordering = ['-date'] 

class Source(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'Sources'


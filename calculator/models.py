from django.db import models

class Offer(models.Model):
    bank_name = models.CharField(max_length=100)
    term_min = models.IntegerField()
    term_max = models.IntegerField()
    rate_min = models.FloatField()
    rate_max = models.FloatField()
    payment_min = models.FloatField()
    payment_max = models.FloatField()
# Create your models here.

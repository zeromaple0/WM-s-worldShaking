from django.db import models


class PrimePrice(models.Model):
    url_name = models.CharField(max_length=50)
    zh_name = models.CharField(max_length=50)
    platinum1 = models.FloatField()
    platinum2 = models.FloatField()
    platinum3 = models.FloatField()
    platinum_avg = models.FloatField(default=0)

from django.db import models


class PrimePriceManager(models.Manager):
    def get_prime_price(self, url_name):
        # 转为需要的字典格式
        return {
            'url_name': url_name,
            'zh_name': self.get(url_name=url_name).zh_name,
            'platinum1': self.get(url_name=url_name).platinum1,
            'platinum2': self.get(url_name=url_name).platinum2,
            'platinum3': self.get(url_name=url_name).platinum3,
            'platinum_avg': self.get(url_name=url_name).platinum_avg
        }

class RivenPriceManager(models.Manager):
    def get_riven_price(self, url_name):
        # 转为需要的字典格式
        return {
            'url_name': url_name,
            'zh_name': self.get(url_name=url_name).zh_name,
            'platinum1': self.get(url_name=url_name).platinum1,
            'platinum2': self.get(url_name=url_name).platinum2,
            'platinum3': self.get(url_name=url_name).platinum3,
            'platinum4': self.get(url_name=url_name).platinum4,
            'platinum5': self.get(url_name=url_name).platinum5,
            'platinum_avg': self.get(url_name=url_name).platinum_avg
        }


class PrimePrice(models.Model):
    url_name = models.CharField(max_length=50)
    zh_name = models.CharField(max_length=50)
    platinum1 = models.FloatField()
    platinum2 = models.FloatField()
    platinum3 = models.FloatField()
    platinum_avg = models.FloatField(default=0)

    objects = PrimePriceManager()



class RivenPrice(models.Model):
    url_name = models.CharField(max_length=50)
    zh_name = models.CharField(max_length=50)
    platinum1 = models.FloatField()
    platinum2 = models.FloatField()
    platinum3 = models.FloatField()
    platinum4 = models.FloatField()
    platinum5 = models.FloatField()
    platinum_avg = models.FloatField(default=0)
    objects = RivenPriceManager()

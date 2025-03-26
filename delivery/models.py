from django.db import models

class SupplyChain(models.Model):
    order_id = models.CharField(max_length=50, unique=True)
    agent_age = models.IntegerField()
    agent_rating = models.FloatField()
    store_latitude = models.FloatField()
    store_longitude = models.FloatField()
    drop_latitude = models.FloatField()
    drop_longitude = models.FloatField()
    order_date = models.DateField()
    order_time = models.TimeField()
    pickup_time = models.TimeField()
    weather = models.CharField(max_length=20)
    traffic = models.CharField(max_length=20)
    vehicle = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    delivery_time = models.IntegerField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"Order {self.order_id} - {self.category}"

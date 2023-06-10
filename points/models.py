from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Kid(models.Model):
    name = models.CharField(max_length=200)
    points = models.IntegerField(default=0)
    points_from_cash = models.IntegerField(default=0)  
    barcode = models.CharField(max_length=200, unique=True) 
    group = models.CharField(max_length=200)  # שדה חדש
    points_history = models.IntegerField(default=0)




    def save(self, *args, **kwargs):
        # if the object already exists, and the points value has changed, create a new PointHistory entry
        if self.pk is not None:
            orig = Kid.objects.get(pk=self.pk)
            if orig.points != self.points:
                PointHistory.objects.create(kid=self, points=self.points, timestamp=timezone.now())
        
        super().save(*args, **kwargs)

class PointHistory(models.Model):
    kid = models.ForeignKey(Kid, on_delete=models.CASCADE, related_name='history')
    points = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

from django.db import models

class Product(models.Model):
    barcode = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    points_value = models.IntegerField()


class DollarToPoint(models.Model):
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    
class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    kid = models.ForeignKey(Kid, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


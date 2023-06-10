from django.contrib import admin
from .models import Kid, PointHistory, Product, Purchase, DollarToPoint

admin.site.register(Kid)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(DollarToPoint)


import datetime


from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.deletion import CASCADE, PROTECT, RESTRICT




class OrderItem(models.Model):

    item_uid = models.CharField(max_length=20)
    item_quantity = models.CharField(max_length=20)
    item_product_id = models.CharField(max_length=20)
    item_product_type = models.CharField(max_length=20)
    item_product_title = models.CharField(max_length=20)
    # 'Order Item Features': '[]' ??
    item_return_days = models.IntegerField()
    item_exchange_days = models.IntegerField()
    item_product_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_basic_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    item_tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    item_sub_total = models.DecimalField(max_digits=10, decimal_places=2)

    seller_cleared = models.BinaryField(default=False) # if the transaction balance has been cleared with the seller





class OrderItemNote(models.Model):
    notes = models.TextField()
    added_by = models.ForeignKey(User, on_delete=RESTRICT)
    order_item = models.ForeignKey(OrderItem, on_delete=CASCADE)
    date_time = models.DateTimeField(default= datetime.datetime.now)
    





    
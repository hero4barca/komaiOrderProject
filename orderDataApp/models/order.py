
import datetime


from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, RESTRICT


# Create your models here.

class Order(models.Model):

    order_number = models.CharField(max_length=20)
    order_date = models.DateField(null=True, blank=True)
    order_time = models.TimeField(null=True, blank=True)
    
    customer_uid = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=20) # name 1
    customer_email = models.CharField(max_length=20) # change to emailfield

    billing_name = models.CharField(max_length=20) # name 2
    billing_address = models.TextField()
    billing_district = models.CharField(max_length=20)
    billing_state = models.CharField(max_length=20)
    billing_zip_code = models.CharField(max_length=20)
    billing_country = models.CharField(max_length=20)
    billing_phone_No = models.CharField(max_length=20)

    shipping_name = models.CharField(max_length=20)
    shipping_address = models.CharField(max_length=20)
    shipping_district = models.CharField(max_length=20)
    shipping_state = models.CharField(max_length=20)
    shipping_zip_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=20)
    shipping_phone_No = models.CharField(max_length=20)

    order_currency = models.CharField(max_length=20)

    # total for items in the order
    order_total = models.DecimalField(max_digits=10, decimal_places=2)

    order_taxes = models.DecimalField(max_digits=10, decimal_places=2) #
    order_discounts = models.DecimalField(max_digits=10, decimal_places=2)

    # subtotal for order items after applying taxes and discount
    order_subtotal = models.DecimalField(max_digits=10, decimal_places=2) 

    # cost of shipping
    order_shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)

    order_ship_TBD = models.DecimalField(max_digits=10, decimal_places=2)

    # order subtotal + order_shipping cost
    order_cart_total = models.DecimalField(max_digits=10, decimal_places=2)

    # taxes applied to cart
    order_cart_taxes = models.DecimalField(max_digits=10, decimal_places=2)

    # discount applied to cart
    order_cart_discount = models.DecimalField(max_digits=10, decimal_places=2)

    # cart total +/- cart discount, cart taxes
    order_grand_total = models.DecimalField(max_digits=10, decimal_places=2)

    order_coupon_code = models.CharField(max_length=20)
    order_coupon_value = models.DecimalField(max_digits=10, decimal_places=2)

    order_status = models.CharField(max_length=20)
    
    payment_method = models.CharField(max_length=20)
    payment_live = models.BooleanField() #  keep or remove ?

    # amount charged by payment gateway for payment processing
    payment_fee = models.DecimalField(max_digits=10, decimal_places=2)

    # amount successfull paid by customer
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_response = models.TextField()
    payment_successful = models.BooleanField(default=False) 


class OrderNote(models.Model):
    notes = models.TextField()
    added_by = models.ForeignKey(User, on_delete=RESTRICT)
    order = models.ForeignKey(Order, on_delete=CASCADE)
    date_time = models.DateTimeField(default= datetime.datetime.now)
    





    
    

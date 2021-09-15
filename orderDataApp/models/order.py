
import datetime


from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, RESTRICT

#models managers for order model
#@TODO refactor -> fit with data set
class InitiatedOrdersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(order_status='Order Initiated')

class PaidOrdersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(order_status__in =('Shipped', 'Packaged'))

class DeliveredOrdersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(order_status ='Delivered')


# Create your models here.

class Order(models.Model):

    order_number = models.CharField(max_length=20, blank=True, null=True)
    order_date = models.DateField(null=True, blank=True)
    order_time = models.TimeField(null=True, blank=True)
    
    customer_uid = models.CharField(max_length=20, blank=True, null=True)
    customer_name = models.CharField(max_length=20, blank=True, null=True) # name 1
    customer_email = models.CharField(max_length=20, blank=True, null=True) # change to emailfield

    billing_name = models.CharField(max_length=20, blank=True, null=True) # name 2
    billing_address = models.TextField(blank=True, null=True)
    billing_district = models.CharField(max_length=20, blank=True, null=True)
    billing_state = models.CharField(max_length=20, blank=True, null=True)
    billing_zip_code = models.CharField(max_length=20, blank=True, null=True)
    billing_country = models.CharField(max_length=20, blank=True, null=True)
    billing_phone_No = models.CharField(max_length=20, blank=True, null=True)

    shipping_name = models.CharField(max_length=20, blank=True, null=True)
    shipping_address = models.CharField(max_length=20, blank=True, null=True)
    shipping_district = models.CharField(max_length=20, blank=True, null=True)
    shipping_state = models.CharField(max_length=20, blank=True, null=True)
    shipping_zip_code = models.CharField(max_length=20, blank=True, null=True)
    shipping_country = models.CharField(max_length=20, blank=True, null=True)
    shipping_phone_No = models.CharField(max_length=20, blank=True, null=True)

    order_currency = models.CharField(max_length=20, blank=True, null=True)

    # total for items in the order
    order_total = models.DecimalField(max_digits=10, decimal_places=2)

    order_taxes = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) #
    order_discounts = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # subtotal for order items after applying taxes and discount
    order_subtotal = models.DecimalField(max_digits=10, decimal_places=2) 

    # cost of shipping
    order_shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    order_ship_TBD = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # order subtotal + order_shipping cost
    order_cart_total = models.DecimalField(max_digits=10, decimal_places=2)

    # taxes applied to cart
    order_cart_taxes = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # discount applied to cart
    order_cart_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # cart total +/- cart discount, cart taxes
    order_grand_total = models.DecimalField(max_digits=10, decimal_places=2)

    order_coupon_code = models.CharField(max_length=20, blank=True, null=True)
    order_coupon_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    order_status = models.CharField(max_length=20, blank=True, null=True)
    
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    payment_live = models.BooleanField() # default val @TODO

    # amount charged by payment gateway for payment processing
    payment_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # amount successfull paid by customer
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    payment_response = models.TextField(blank=True, null=True)
    payment_successful = models.BooleanField(default=False) # default val @TODO

    # assign managers
    objects = models.Manager() # The default manager.
    initiated_orders = InitiatedOrdersManager()
    paid_orders = PaidOrdersManager()
    delivered_orders = DeliveredOrdersManager()


    def __str__(self) :
        return " | ".join([self.order_number, str(self.order_date), self.customer_name, 
                            str(self.payment_amount), str(self.order_grand_total ), str(self.order_cart_discount) ])


class OrderNote(models.Model):
    notes = models.TextField()
    added_by = models.ForeignKey(User, on_delete=RESTRICT)
    order = models.ForeignKey(Order, on_delete=CASCADE)
    date_time = models.DateTimeField(default= datetime.datetime.now)
    





    
    

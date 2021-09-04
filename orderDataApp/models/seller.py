from django.db import models
from django.conf import settings


class Seller(models.Model):

    seller_uid = models.CharField(max_length=20)
    seller_unique_code = models.CharField(max_length=20)   
    seller_name = models.CharField(max_length=20)
    seller_company = models.CharField(max_length=20)
    seller_email = models.CharField(max_length=20)
    


class SellerDetail(models.Model):

    Seller = models.ForeignKey(Seller, on_delete=models.RESTRICT) 
    active = models.BooleanField(default=True)
    notes = models.TextField()
    
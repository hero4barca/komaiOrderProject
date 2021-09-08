import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.deletion import CASCADE, RESTRICT, SET_DEFAULT, SET_NULL



class Seller(models.Model):
    
    seller_uid = models.CharField(max_length=20)
    seller_unique_code = models.CharField(max_length=20)   
    seller_name = models.CharField(max_length=20)
    seller_company = models.CharField(max_length=20)
    seller_email = models.CharField(max_length=20)
    

class BankAccount(models.Model):
    account_name = models.TextField()
    account_number = models.CharField(max_length=20)
    bank_name = models.TextField()
    bank_address = models.TextField()
    swift_code = models.CharField(max_length=20)
    iban_code = models.CharField(max_length=20)
    other_details = models.TextField()

class SellerDetail(models.Model):

    Seller = models.OneToOneField(Seller, on_delete=models.RESTRICT) 
    active = models.BooleanField(default=True)
    uncleared_balance = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    bank_account = models.OneToOneField(BankAccount, on_delete=SET_DEFAULT, null=True, default=None)
    

class SellerNote(models.Model):

    seller_detail = models.ForeignKey(SellerDetail, on_delete=CASCADE)
    note = models.TextField()
    added_by = models.ForeignKey(User, on_delete=RESTRICT)
    date_time = models.DateTimeField(default=datetime.datetime.now)

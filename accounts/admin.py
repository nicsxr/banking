from django.contrib import admin
from accounts.models import Account, Transaction, Card

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Card)
# Register your models here.
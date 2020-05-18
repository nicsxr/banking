from django.contrib import admin
from accounts.models import Account, Transaction

admin.site.register(Account)
admin.site.register(Transaction)
# Register your models here.
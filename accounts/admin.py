
from django.contrib import admin
from . models import Account, APIKey

class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'sms_provider_title', 'username', 'merchant_code']
    list_filter = ['sms_provider_title']

class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['public_key', 'private_key', 'is_active']
    list_filter = ['is_active']

admin.site.register(Account, AccountAdmin)
admin.site.register(APIKey, APIKeyAdmin)
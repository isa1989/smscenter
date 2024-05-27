from django.db import models
import uuid
import base64

from provider.models import SMSProviderTitle




class Account(models.Model):
    name = models.CharField(max_length=200, blank=False, verbose_name='Name')
    sms_provider_title = models.ForeignKey(SMSProviderTitle, blank=False, null=True, on_delete=models.SET_NULL, verbose_name='SMS provider title')
    username = models.CharField(max_length=500, blank=False, verbose_name='Username')

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
    
    def __str__(self):
        return self.name




class APIKey(models.Model):
    account = models.ForeignKey('Account', blank=False, null=True, related_name="apikey", on_delete=models.SET_NULL, verbose_name='Account')
    public_key = models.CharField(max_length=500, blank=True, verbose_name='Public key')
    private_key = models.CharField(max_length=500, blank=True, verbose_name='Private key')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'API key'
        verbose_name_plural = 'API keys'
    
    def __str__(self):
        return self.public_key

    def __init__(self, *args, **kwargs):
        super(APIKey, self).__init__(*args, **kwargs)
        self.cache_is_active = self.is_active
    

    def save(self, *args, **kwargs):
        
        if not self.public_key:
            self.public_key = str(uuid.uuid4())

        if not self.private_key:
            uuid_str = str(uuid.uuid4())
            uuid_bytes = uuid_str.encode('utf-8')
            base64_bytes = base64.urlsafe_b64encode(uuid_bytes)
            self.private_key = base64_bytes.decode('utf-8')
        
        super(APIKey, self).save(*args, **kwargs)

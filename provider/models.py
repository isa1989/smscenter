
from django.db import models
from solo.models import SingletonModel
from random import randint




class MobisSettings(SingletonModel):
    login = models.CharField(max_length=120, blank=False)
    password = models.CharField(max_length=120, blank=False)

    class Meta:
        verbose_name = 'Mobis settings'
        verbose_name_plural = 'Mobis settings'
    
    def __str__(self):
        return 'Mobis settings'




class MobisSMSControlid(models.Model):
    control_id = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return str(self.control_id)

    def save(self, *args, **kwargs):
        
        merchant_code = str(kwargs.pop('code', 1234))

        if self.control_id is None or self.control_id == '':
            self.control_id = merchant_code + str(randint(10000000000000000000, 100000000000000000000))

        unique_control_id = self.control_id

        while MobisSMSControlid.objects.filter(control_id=unique_control_id).exists():
            unique_control_id = merchant_code + str(randint(10000000000000000000, 100000000000000000000))

        self.control_id = unique_control_id

        return super(MobisSMSControlid, self).save(*args, **kwargs)




class SMSProviderTitle(models.Model):
    title = models.CharField(max_length=200, blank=False, verbose_name='Title')

    class Meta:
        verbose_name = 'SMS provider title'
        verbose_name_plural = 'SMS provider titles'
    
    def __str__(self):
        return self.title




class SMS(models.Model):
    control_id = models.CharField(max_length=120, blank=True, null=True)
    account = models.ForeignKey('accounts.Account', blank=False, null=True, on_delete=models.SET_NULL)
    api_key = models.ForeignKey('accounts.APIKey', blank=False, on_delete=models.PROTECT)
    msisdn = models.CharField(max_length=120, blank=True, null=True)
    is_bulk = models.BooleanField(default=False)


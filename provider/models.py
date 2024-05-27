
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


class SMSProviderTitle(models.Model):
    title = models.CharField(max_length=200, blank=False, verbose_name='Title')

    class Meta:
        verbose_name = 'SMS provider title'
        verbose_name_plural = 'SMS provider titles'
    
    def __str__(self):
        return self.title




class SMS(models.Model):
    STATUS_CHOICES = [
        ('0', 'checking'),
        ('1', 'queued'),
        ('2', 'delivered'),
        ('3', 'failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True, verbose_name='Status')
    control_id = models.CharField(max_length=120, blank=True, null=True)
    account = models.ForeignKey('accounts.Account', blank=False, null=True, on_delete=models.SET_NULL)
    api_key = models.ForeignKey('accounts.APIKey', blank=False, on_delete=models.PROTECT)
    msisdn = models.TextField(max_length=120, blank=True, null=True)
    task_id = models.CharField(max_length=120, blank=True, null=True)
    is_bulk = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'SMS'
        verbose_name_plural = 'SMS'

    # def __str__(self):
    #     return self.account.username
    



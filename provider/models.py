
from django.db import models




class SMSProviderTitle(models.Model):
    title = models.CharField(max_length=200, blank=False, verbose_name='Title')

    class Meta:
        verbose_name = 'SMS provider title'
        verbose_name_plural = 'SMS provider titles'
    
    def __str__(self):
        return self.title
    

from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import APIKey

@receiver(post_save, sender=APIKey)
def api_key_post_save(sender, instance ,created, **kwargs):
    if instance.is_active == True:
        APIKey.objects.filter(account=instance.account).exclude(id=instance.id).update(is_active=False)
 
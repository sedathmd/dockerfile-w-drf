from django.db import models
from django.contrib.auth.models import User

#sinyal kutuphaneleri
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    #onetoonefield sadece bir hesap olusturulabilmesi icin
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=200)
    address = models.CharField(max_length=120)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


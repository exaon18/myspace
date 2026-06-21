from django.db import models

class Myuser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    tgID = models.IntegerField(unique=True)
    picture = models.URLField(blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    hmac=models.CharField(max_length=255, blank=True, null=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
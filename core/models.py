from django.db import models

class Myuser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    tgID = models.IntegerField(unique=True)
    picture = models.URLField(blank=True, null=True)
    

    def __str__(self):
        return self.username
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=255, verbose_name="Full Name")

    def __str__(self):
        return self.fullname or self.username
    
class Criterios(models.Model):
    id = models.AutoField(primary_key=True)
    criterion = models.CharField(max_length=255)
    stage = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=512)
    place_of_study = models.CharField(max_length=512)
    teacher_full_name = models.CharField(max_length=512, blank=True, null=True, default=None)
    teacher_phone = models.CharField(max_length=14, blank=True, null=True, default=None)

class Scores(models.Model):
    id = models.AutoField(primary_key=True)
    stage = models.SmallIntegerField()
    score = models.CharField(max_length=512)
    participiant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='Participiant')
    juri_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='Juri')
    criterion_id = models.ForeignKey(Criterios, on_delete=models.CASCADE, related_name='Criterion')

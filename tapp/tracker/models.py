from django.db import models 
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    name= models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at =models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    


class TimeEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project =models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    start_time =models.TimeField()
    end_time = models.TimeField(null= True, blank= True)
    duration = models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.project.name}"
    
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_employee = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

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
    start_time =models.DateTimeField()
    end_time = models.DateTimeField(null= True, blank= True)
    duration = models.DateTimeField(null=True,blank= True)
    def __str__(self):
        return f"{self.user.username} - {self.project.name}"
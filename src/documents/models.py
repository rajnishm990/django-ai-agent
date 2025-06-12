from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Document(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300 , default='Title')
    content = models.TextField(blank=True, null= True)
    active = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True) #updates time on just instance creation 
    updated_at = models.DateTimeField(auto_now=True)  #updates time on every change or update 
    





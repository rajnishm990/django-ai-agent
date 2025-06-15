from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL



class Document(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300 , default='Title')
    content = models.TextField(blank=True, null= True)
    active = models.BooleanField(default=True) 
    active_at = models.DateTimeField(auto_now_add=False , auto_now=False, blank =True , null=True)
    created_at = models.DateTimeField(auto_now_add=True) #updates time on just instance creation 
    updated_at = models.DateTimeField(auto_now=True)  #updates time on every change or update 

    def save(self,*args , **kwargs):
        if self.active and self.active_at is None:
            self.active_at = timezone.now()
        else:
            self.active_at = None 
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    







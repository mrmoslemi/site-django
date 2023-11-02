from django.db import models

class Author(models.Model):
    class Meta:
        ordering = ['user_title']
    
    
    user_title = models.CharField(max_length=50)
    bio = models.TextField()
    
    def __str__(self):
        return self.user_title
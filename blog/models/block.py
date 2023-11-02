from django.db import models

class Block(models.Model):
    section = models.ForeignKey(to='blog.Section', on_delete=models.CASCADE)
    
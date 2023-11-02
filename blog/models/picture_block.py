from django.db import models
from .block import Block
from PIL import Image as PilImage

class PictureBlock(Block):
    picture = models.ImageField(upload_to='pictures/')
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        picture = PilImage.open(self.picture)
        resized = picture.resize((800, 600)) # smaller size
        resized.save(f'{self.picture.path}_small.jpg')
        
        thumbnail = picture.resize((200, 200))
        thumbnail.save(f'{self.picture.path}_thumb.jpg')
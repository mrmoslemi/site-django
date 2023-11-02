from django.db import models
from .block import Block

class ParagraphBlock(Block):
    text_body = models.TextField()
from django.db import models
from .block import Block

class TableBlock(Block):
    table = models.JSONField()
from django.db import models
from utils import mixins as util_models


# method 4

class Keyword(models.Model):
    title = util_models.PhraseField()
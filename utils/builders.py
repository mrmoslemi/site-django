import string
from datetime import timedelta
from django.utils import timezone
def random(length:int = 32, charset:str =string.ascii_letters+string.digits ):
    import random as rand
    #TODO
    return "aaaaaa"

def future(seconds:int = 60):
    return timezone.now() + timedelta(seconds=seconds)

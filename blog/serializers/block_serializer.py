from rest_framework import serializers
from blog.models import Block

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['__all__']
from rest_framework import serializers
from blog.models import ParagraphBlock
from blog.serializers.block_serializer import BlockSerializer

class ParagraphBlockSerializer(BlockSerializer):
    class Meta(BlockSerializer.Meta):
        model = ParagraphBlock
        fields = BlockSerializer.Meta.fields + ['text_body']
    
    text_body = serializers.CharField()
    
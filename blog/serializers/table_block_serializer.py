from rest_framework import serializers
from blog.models import TableBlock
from blog.serializers.block_serializer import BlockSerializer

class TableBlockSerializer(BlockSerializer):
    class Meta(BlockSerializer.Meta):
        model = TableBlock
        fields = BlockSerializer.Meta.fields + ['table']
    
    table = serializers.JSONField()
    
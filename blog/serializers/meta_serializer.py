from rest_framework import serializers
from blog.models import Meta

class MetaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Meta
        fields = ['__all__']
        
    meta_keywords = serializers.CharField(required=False)
    meta_description = serializers.CharField(required=False)
    
    created_at = serializers.DateTimeField(read_only=True)
    upload_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        return Meta.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.meta_keywords = validated_data.get('meta_keywords', instance.meta_keywords)
        instance.meta_description = validated_data.get('meta_description', instance.meta_description)
        instance.save()
        return instance
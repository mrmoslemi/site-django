from rest_framework import serializers
from blog.models import Article, Author
from blog.serializers.article_serializer import ArticleSerializer

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['__all__']
        
    articles = ArticleSerializer(many=True, read_only=True)
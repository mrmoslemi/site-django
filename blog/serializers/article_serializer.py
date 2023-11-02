from rest_framework import serializers
from blog.models import Article, ArticleCategory

class ArticleSerializer(serializers.HyperlinkModelSerializer):
    class Meta:
        model = Article
        fields = ['__all__']
        
    author = serializers.StringRelatedField()
    categories = serializers.SlugRelatedField(
        many=True,
        queryset=ArticleCategory.objects.all(),
        read_only=True,
        slug_field='name'
    )

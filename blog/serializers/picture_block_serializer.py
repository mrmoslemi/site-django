from requests import Response
from rest_framework import viewsets, serializers
from blog.models import PictureBlock
from blog.serializers.block_serializer import BlockSerializer

class PictureBlockViewSet(viewsets.ModelViewSet):
    queryset = PictureBlock.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=Response.status.HTTP_201_CREATED, headers=headers)
    
class PictureBlockSerializer(BlockSerializer):
    class Meta(BlockSerializer.Meta):
        model = PictureBlock
        fields = BlockSerializer.Meta.fields + ['picture']
    
    picture = serializers.ImageField(use_url=True)
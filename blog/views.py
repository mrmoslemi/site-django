from django.shortcuts import render
from blog.serializers.picture_block_serializer import PictureBlockSerializer

serializer = PictureBlockSerializer()
serializer.data['picture']
serializer.data['small']
serializer.data['thumb']
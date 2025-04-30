from rest_framework import serializers
from .models import Tag, Document

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class DocumentSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ('id', 'title', 'content', 'tags', 'created_at', 'updated_at')
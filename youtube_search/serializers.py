from rest_framework import serializers

from .models import YoutubeVideo, Tag

class KWSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

class YTVideoSerializer(serializers.ModelSerializer):

    key_words = KWSerializer(read_only=True, many=True)

    class Meta:
        model = YoutubeVideo
        fields = ('id', 'video', 'published_at', 'title', 'description', 'thumb_url', 'key_words')
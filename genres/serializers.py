from rest_framework import serializers

from authentication.serializers import UserReadSerializer as UserSerializer

from .models import Genre


class GenreReadSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = "__all__"

    def get_created_by(self, obj):
        return UserSerializer(obj.created_by).data


class GenreWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']
        read_only_fields = ['id']

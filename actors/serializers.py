from rest_framework import serializers

from authentication.serializers import UserReadSerializer as UserSerializer

from .models import Actor


class ActorReadSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Actor
        fields = "__all__"

    def get_created_by(self, obj):
        return UserSerializer(obj.created_by).data


class ActorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name']
        read_only_fields = ['id']

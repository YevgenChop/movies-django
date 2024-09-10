from rest_framework import serializers

from authentication.serializers import UserReadSerializer as UserSerializer

from genres.models import Genre
from genres.serializers import GenreReadSerializer

from actors.models import Actor
from actors.serializers import ActorReadSerializer

from .models import Movie


class MovieWriteActorSerializer(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Actor.objects.all().filter(
            created_by=self.context['request'].user
        )

    def to_representation(self, value):
        super().to_representation(value)
        return ActorReadSerializer(value).data

    def to_internal_value(self, data):
        super().to_internal_value(data)
        return Actor.objects.get(id=data)


class MovieWriteGenreSerializer(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Genre.objects.all().filter(
            created_by=self.context['request'].user
        )

    def to_representation(self, value):
        super().to_representation(value)
        return GenreReadSerializer(value).data

    def to_internal_value(self, data):
        super().to_internal_value(data)
        return Genre.objects.get(id=data)


class MovieReadSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    genres = GenreReadSerializer(many=True, read_only=True)
    actors = ActorReadSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'


class MovieWriteSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    genres = MovieWriteGenreSerializer(
        many=True,
        queryset=Genre.objects.all()
    )
    actors = MovieWriteActorSerializer(
        many=True,
        queryset=Actor.objects.all()
    )

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ['id', 'created_by']

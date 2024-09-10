from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Movie
from .serializers import (
    MovieReadSerializer, MovieWriteSerializer,
)


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieReadSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by=self.request.user)

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        sort_field = self.request.GET.get('sort_field')
        sort_direction = self.request.GET.get('sort_direction')
        if sort_field:
            if sort_direction == 'desc':
                sort_field = f'-{sort_field}'

            queryset = queryset.order_by(sort_field)

        return queryset


class MovieRetrieveView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queyset = self.queryset.filter(created_by=self.request.user)
        print(queyset.query)
        return queyset


class MovieCreateView(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieWriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MovieUpdateView(generics.UpdateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieWriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class MovieDestroyView(generics.DestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieWriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class MovieDestroyListView(generics.GenericAPIView):
    queryset = Movie.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        self.get_queryset().filter(id__in=request.data.get('ids', [])).delete()
        return Response(status=204)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

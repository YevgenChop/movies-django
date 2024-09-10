from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Genre
from .serializers import (
    GenreReadSerializer, GenreWriteSerializer,
)


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreReadSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by=self.request.user)

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        sort_field = self.request.GET.get('sort_field')
        sort_direction = self.request.GET.get('sort_direction')
        if sort_field:
            if sort_direction == 'descending':
                sort_field = f'-{sort_field}'

            queryset = queryset.order_by(sort_field)

        return queryset


class GenreRetrieveView(generics.RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class GenreCreateView(generics.CreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreWriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class GenreUpdateView(generics.UpdateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreWriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        print(self.request.user)
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class GenreDestroyView(generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreWriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class GenreDestroyListView(generics.GenericAPIView):
    queryset = Genre.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        self.get_queryset().filter(id__in=request.data.get('ids', [])).delete()
        return Response(status=204)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

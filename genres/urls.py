from django.urls import path

from .views import (
    GenreListView,
    GenreRetrieveView,
    GenreCreateView,
    GenreUpdateView,
    GenreDestroyView,
    GenreDestroyListView,
)

urlpatterns = [
    path('', GenreListView.as_view(), name='genre_list'),
    path('create/', GenreCreateView.as_view(),
         name='genre_create'),
    path('<int:pk>/details', GenreRetrieveView.as_view(),
         name='genre_retrieve'),
    path('<int:pk>/update', GenreUpdateView.as_view(),
         name='genre_update'),
    path('<int:pk>/delete', GenreDestroyView.as_view(),
         name='genre_delete'),
    path('delete_many', GenreDestroyListView.as_view(),
         name='genre_delete_many'),
]

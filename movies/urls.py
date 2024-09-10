from django.urls import path

from .views import (
    MovieListView,
    MovieCreateView,
    MovieRetrieveView,
    MovieUpdateView,
    MovieDestroyView,
    MovieDestroyListView,
)

urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('create/', MovieCreateView.as_view(), name='movie_create'),
    path('<int:pk>/details', MovieRetrieveView.as_view(),
         name='movie_retrieve'),
    path('<int:pk>/update', MovieUpdateView.as_view(),
         name='movie_update'),
    path('<int:pk>/delete', MovieDestroyView.as_view(),
         name='movie_delete'),
    path('delete_many', MovieDestroyListView.as_view(),
         name='movie_delete_many'),
]

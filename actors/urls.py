from django.urls import path

from .views import (
    ActorListView,
    ActorRetrieveView,
    ActorCreateView,
    ActorUpdateView,
    ActorDestroyView,
    ActorDestroyListView,
)

urlpatterns = [
    path('', ActorListView.as_view(), name='actor_list'),
    path('create/', ActorCreateView.as_view(),
         name='actor_create'),
    path('<int:pk>/details', ActorRetrieveView.as_view(),
         name='actor_retrieve'),
    path('<int:pk>/update', ActorUpdateView.as_view(),
         name='actor_update'),
    path('<int:pk>/delete', ActorDestroyView.as_view(),
         name='actor_delete'),
    path('delete_many', ActorDestroyListView.as_view(),
         name='actor_delete_many'),
]

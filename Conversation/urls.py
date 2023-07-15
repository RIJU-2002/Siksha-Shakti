from django.urls import path
from .views import MessageCreateView,MessageListView

urlpatterns = [
    path('messages/create/<str:receiver_name>/', MessageCreateView.as_view(), name='create-message'),
    path('messages/<str:receiver_name>/',MessageListView.as_view(),name='fetch-message')
]

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import *


urlpatterns = [
    path('login/', LoginPageView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogOutView.as_view(), name='logout'),
    
    path('', HomeView.as_view(), name='home'),
    path('room/<str:pk>/',RoomView.as_view(), name='room'),
    path('profile/<str:pk>/', UserProfileView.as_view(), name='user-profile'),
    
    path('create-room/', CreateRoomView.as_view(), name='create-room'), 
    path('update-room/<str:pk>', UpdateRoomView.as_view(), name='update-room'),
    path('delte-room/<str:pk>', DeleteRoomView.as_view(), name='delete-room'), 
    path('delte-message/<str:pk>',DeleteMessageView.as_view(), name='delete-message'), 
    path('update-user/<str:pk>/', UpdateUserView.as_view(), name='update-user'), 
    
    path('topic/', TopicPageView.as_view(), name='topic-page'), 
    path('activity/', ActivityPageView.as_view(), name='activity-page'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
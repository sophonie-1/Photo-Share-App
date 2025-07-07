from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('',GalleryView.as_view(),name='gallery'),
    path('<int:pk>/',DetailImageView.as_view(),name='image'),
    path('create/',CreateFormView.as_view(),name='create'),
    path('<int:pk>/update-image/',PhotoUpdateView.as_view(),name='update-image'),
    path('<int:pk>/delete-image',DeleteImageView.as_view(),name='delete-image'),


    path('login/',LoginCustomView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('register/',RegisterView.as_view(),name='register'),

    path('comment/<int:pk>/',CommentView.as_view(),name='comment'),
 
]

    
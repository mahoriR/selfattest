
from django.urls import path
from . import views

app_name = 'media_photo'

urlpatterns = [

    #   POST - Upload photos for attesting
    path(r'attested', views.UserPhotoListView.as_view(), name='handler-user-photo-list'),
]

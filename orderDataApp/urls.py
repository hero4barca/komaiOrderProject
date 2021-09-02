from django.urls import path
from orderDataApp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("upload_csv_file/", views.upload_csv_file, name="upload_csv_file" ),
    path("extract_data/", views.extract_data, name="extract_data"),
    path("show_data/", views.show_data,  name="show_data"),
]
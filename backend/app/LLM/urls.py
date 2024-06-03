from . import views
from django.urls import path

urlpatterns = [
    path("querygpt35/", views.query_gpt35, name="querygpt35"),
    path("querygpt4/", views.query_gpt4, name="querygpt4"),
    path("queryllama/", views.query_llama, name="queryllama"),
    path("queryfalcon/", views.query_falcon, name="queryfalcon"),
    path("stream/", views.stream, name="stream")
]
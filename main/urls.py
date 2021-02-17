from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
path("", views.home_page, name='home_page'),
path("sudoku/", views.sudoku, name='sudoku'),
]

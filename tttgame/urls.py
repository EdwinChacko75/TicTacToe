from django.urls import path
from . import views

urlpatterns = [
    path('', views.makeBoard, name='tttgame'), 
    path('tttgame/api/makeMove/', views.makeMove, name='make_move')
]


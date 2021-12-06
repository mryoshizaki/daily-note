from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    #notes
    path('view-notes/', views.Notes_View, name='notesview'),
]

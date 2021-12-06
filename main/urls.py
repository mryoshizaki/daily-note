from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('reset/password-reset/', views.passwordReset, name="password-reset"),
    path('reset/password-reset/done/', views.PasswordResetDoneView.as_view(template_name='main/reset/reset-password/password-reset-done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name="main/reset/reset-password/password-reset-confirm.html"), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(template_name='main/reset/reset-password/password-reset-complete.html'), name='password_reset_complete'),      

    #notes
    path('view-notes/', views.Notes_View, name='notesview'),
    path('view-notes/update/<pk>', views.update_note, name='update-note'),
    path('view-notes/delete/<pk>', views.delete_note, name='delete-note'),
]

from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('reset/password-reset/', views.passwordReset, name="password-reset"),
    path('reset/password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/reset/password-reset-done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="main/reset/password-reset-confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/reset/password-reset-complete.html'), name='password_reset_complete'),      

    #notes
    path('view-notes/', views.Notes_View, name='notesview'),
    path('view-notes/update/<pk>', views.update_note, name='update-note'),
#    path('view-notes/cancel-update-notes', views.Cancel_Update_Notes, name='cancel-update-notes'),
    path('view-notes/delete/<pk>', views.delete_note, name='delete-note'),
    path('tinymce/', include('tinymce.urls')),
    
    #calendar
    # path('create-event/', views.create_event, name='calendar'),
    path('calendar-view/', views.CalendarView.as_view(), name='calendar'),
    # path('calendar-view/<int>', views.CalendarView.as_view(), name='calendar'),
    path('create-event/', views.create_event, name='create-event'),
	# path(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path('view-calendar/update/<pk>', views.update_event, name='update-event'),
    path('view-calendar/delete/<pk>', views.delete_event, name='delete-event'),

    #color-theme
    path('pastel-themed/',views.Pastel_Themed,name='pastel-themed'),
    path('neutral-themed/',views.Neutral_Themed,name='neutral-themed'),
    path('bright-themed/',views.Bright_Themed,name='bright-themed'),

    #dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    #help
    path('help/about-daily-note', views.about, name='about'),
    path('help/dashboard', views.help_dashboard, name='helpdash'),
    path('help/calendar', views.help_calendar, name='helpcal'),
    path('help/notes', views.help_notes, name='helpnotes'),
    path('help/themes', views.help_themes, name='helpthemes'),
    
]

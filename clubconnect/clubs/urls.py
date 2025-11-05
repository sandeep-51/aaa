from django.urls import path
from . import views

urlpatterns = [
    path('', views.clubs_list, name='clubs_list'),
    path('create/', views.create_club, name='create_club'),
    path('<int:club_id>/assign-founder/', views.assign_founder, name='assign_founder'),
    path('<int:club_id>/', views.club_detail, name='club_detail'),
    path('<int:club_id>/edit/', views.edit_club, name='edit_club'),
    path('search/', views.search_clubs, name='search_clubs'),
    path('<int:club_id>/register/', views.register_for_club, name='register_for_club'),
    path('<int:club_id>/message-founder/', views.send_message_to_founder, name='message_founder'),
    path('<int:club_id>/create-event/', views.create_event, name='create_event'),
    path('<int:club_id>/chat/', views.club_chat, name='club_chat'),
    path('membership/<int:membership_id>/approve/', views.approve_membership, name='approve_membership'),
    path('<int:club_id>/leave/', views.leave_club, name='leave_club'),
    path('membership/<int:membership_id>/reject/', views.reject_membership, name='reject_membership'),
    path('<int:club_id>/create-announcement/', views.create_club_announcement, name='create_club_announcement'),
    path('announcement/<int:announcement_id>/delete/', views.delete_club_announcement, name='delete_club_announcement'),
]
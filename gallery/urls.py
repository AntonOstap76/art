from django.urls import path
from . import views  

urlpatterns = [

    path("", views.gallery, name="gallery"),
    path("info/", views.info, name="info"),
    path("create/", views.create_art, name="create"),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    # path('profile/liked/', views.liked, name='liked_arts'),
    path("edit/<int:pk>/", views.edit, name="edit"),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('art/<int:pk>/', views.art, name='art'),
    # path('art/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),                 
    path('profile/edit/', views.edit_profile, name='edit_profile'),       
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('toggle_like/<int:pk>/', views.toggle_like, name='toggle_like'),
    path ('liked/', views.liked, name="liked"),

      
]
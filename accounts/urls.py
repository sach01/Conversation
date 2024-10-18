from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),  # URL for user registration
    path('login/', views.login_view, name='login'),  # URL for user login
    path('logout/', views.logout_view, name='logout'),  # URL for user logout
    path('users/', views.user_list, name='user_list'),  # URL for user list (admin)
    path('assign_role/<int:user_id>/<str:role>/', views.assign_role, name='assign_role'),  # URL to assign roles
    path('no_permission/', views.no_permission, name='no_permission'),
]

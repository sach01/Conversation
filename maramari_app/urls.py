
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import import_csv, list_data
#from django.contrib.auth import views as auth_views

#from .views import CustomTokenObtainPairView, logout_view, register_user
#from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('test-page/', views.test_page, name='test-page'),
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('import/', import_csv, name='import_csv'),  # Ensure this pattern exists
    path('list/', list_data, name='list_data'),

    path('translate/', views.translate_view, name='translate'),
    path('submit_translation/<int:sentence_pair_id>/', views.submit_translation, name='submit_translation'),
    path('analytics/', views.analytics_view, name='analytics'),

    path('dashboard/', views.dashboard, name='dashboard'),
    

]



from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import import_csv, list_data

urlpatterns = [
    path('test-page/', views.test_page, name='test-page'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('import/', import_csv, name='import_csv'),  # Ensure this pattern exists
    path('list/', list_data, name='list_data'),

]


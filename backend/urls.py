from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import UserAuthViewSet, RegisterView, LogoutView ,CustomTokenObtainPairView

# ใช้ DefaultRouter สำหรับ ViewSet
router = DefaultRouter()
router.register(r'users', UserAuthViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Authentication
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Register & Logout
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/logout/', LogoutView.as_view(), name='logout'),

    # ViewSet
    path('api/', include(router.urls)),
]

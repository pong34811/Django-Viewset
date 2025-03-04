from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        if not self.user.is_authenticated:
            raise serializers.ValidationError({"error": "User is not authenticated"})
            
        return {
            "tokens": {"access": data["access"], "refresh": data["refresh"]},
            "user": {
                "id": self.user.id,
                "username": self.user.username,
                "email": self.user.email or "No email provided"
            }
        }

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserAuthViewSet(viewsets.ModelViewSet):
    """
    ViewSet สำหรับการจัดการผู้ใช้ (ดึงข้อมูล, แก้ไข, ลบ) เฉพาะข้อมูลของตัวเอง
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        ✅ แสดงเฉพาะข้อมูลของผู้ใช้ที่ล็อกอิน
        """
        return User.objects.filter(id=self.request.user.id)

class RegisterView(generics.CreateAPIView):
    """
    API สำหรับสมัครสมาชิก
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # ไม่ต้องล็อกอิน

class LogoutView(APIView):
    """
    API สำหรับ Logout (Blacklisting Token)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # เพิ่ม Token ลง blacklist
            return Response({"message": "Logged out successfully"}, status=200)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema

User = get_user_model()

class NoAuthTokenView(APIView):
    @extend_schema(
        tags=['Testing'],
        methods=["GET"],
        description='Get Testing User Tokens',
    )
    
    def get(self, request):
        user = User.objects.filter(is_superuser=True).first()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })
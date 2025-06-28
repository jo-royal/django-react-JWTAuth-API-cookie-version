from django.forms import ValidationError
from .utils import generate_reset_code, send_password_reset_email
from .permissions import BrandOwner, IsBrandActive, IsUser
from .serializers import BrandProfileSerializer, ChangePasswordSerializer, ConfirmPasswordResetSerializer, CreateUserSerializer, RequestPasswordResetSerializer, UserProfileSerializer, LoginUserSerializer, UserSerializer
from .models import BrandProfile, CustomAccounts, UserProfile
from rest_framework import generics, permissions, views, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model
from django.core.cache import caches


User = get_user_model()

cache = caches['default']




# Create your views here.
class CreateUser(generics.CreateAPIView):
    queryset = CustomAccounts.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.AllowAny]


#####################
class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            response = Response({
                "user": UserSerializer(user).data},
                                status=status.HTTP_200_OK)
            
            response.set_cookie(key="access_token", 
                                value=access_token,
                                httponly=True,
                                secure=True,
                                samesite="None")
            
            response.set_cookie(key="refresh_token",
                                value=str(refresh),
                                httponly=True,
                                secure=True,
                                samesite="None",
                                )  # 1 week
            return response
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(views.APIView):
    
    def post(self, request):
        print("LogoutView called")
        refresh_token = request.COOKIES.get("refresh_token")
        print("refresh_token", refresh_token)
        if not refresh_token:
             print("refresh_token not found in cookies")
        
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
            except Exception as e:
                return Response({"error":"Error invalidating token:" + str(e) }, status=status.HTTP_400_BAD_REQUEST)
        
        response = Response({"message": "Successfully logged out!"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        
        return response    

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request):
        
        refresh_token = request.COOKIES.get("refresh_token")
        
        if not refresh_token:
            return Response({"error":"Refresh token not provided"}, status= status.HTTP_401_UNAUTHORIZED)
    
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            
            response = Response({"message": "Access token token refreshed successfully"}, status=status.HTTP_200_OK)
            response.set_cookie(key="access_token", 
                                value=access_token,
                                httponly=True,
                                secure=True,
                                samesite="None")
            return response
        except InvalidToken:
            return Response({"error":"Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        
    
#########################



class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    

    def perform_create(self, serializer):
        queryset = UserProfile.objects.filter(user=self.request.user)
        if queryset.exists():
            raise ValidationError("please send patch or put request to update your profile.")
        serializer.save(user=self.request.user)


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]

    def get_object(self):
        # Use the authenticated user to retrieve their profile
        return UserProfile.objects.get(user=self.request.user)
    


class BrandProfileView(generics.CreateAPIView):
    queryset = BrandProfile.objects.all()
    serializer_class = BrandProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsBrandActive]

    def perform_create(self, serializer):
        queryset = BrandProfile.objects.filter(owner=self.request.user)
        if queryset.exists():
           raise ValidationError("please send patch or put request to update your profile.")
        serializer.save(owner=self.request.user)


class BrandsView(generics.ListAPIView):
    queryset = BrandProfile.objects.all()
    serializer_class = BrandProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BrandView(generics.RetrieveAPIView):
    queryset = BrandProfile.objects.all()
    serializer_class = BrandProfileSerializer
    lookup_field = "username"
    lookup_url_kwarg = "username"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

class BrandGetUpdateView(generics.RetrieveUpdateAPIView):
    queryset = BrandProfile.objects.all()
    serializer_class = BrandProfileSerializer
    permission_classes = [permissions.IsAuthenticated, BrandOwner]

    def get_object(self):
        return BrandProfile.objects.get(owner=self.request.user)
    

###################################### request password reset view
class RequestPasswordResetView(views.APIView):


    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = generate_reset_code()
        cache.set(f"pwd_reset_{email}", code, timeout=600)  # 10 minutes
        send_password_reset_email(email, code)
        return Response({"detail": "Reset code sent to email."}, status=status.HTTP_200_OK)


# views.py
class ConfirmPasswordResetView(views.APIView):
    def post(self, request):
        serializer = ConfirmPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)



class ChangePasswordView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password updated successfully."})
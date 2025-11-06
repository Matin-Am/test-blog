from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from mail_templated import EmailMessage
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .serializers import (RegistrationSerializer,
                          CustomTokenSerializer,CustomTokenObtainPairSerializer,
                          ChangepasswordSerializer,ProfileSerializer)
from .utils import EmailThread
from ...models import Profile

class RegistrationAPIView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serialzier = self.serializer_class(data=request.data)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serialzier.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors,status=status.HTTP_400_BAD_REQUEST)
    
class CustomObtainTokenView(ObtainAuthToken):
    serializer_class = CustomTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token":token.key , 
            "email": user.email , 
            "user_id": user.id
        })


class CustomDiscardTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        request.user.auth_token.delete()
        return Response({"Message":"Token deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    



class CustomJwtTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(APIView):
    serializer_class = ChangepasswordSerializer
    permission_classes = [IsAuthenticated,]

    def post(self,request):
        user = request.user
        serilaizer = self.serializer_class(data=request.data)
        serilaizer.is_valid(raise_exception=True)
        if not user.check_password(raw_password=serilaizer.validated_data.get("old_password")):
            return Response({"Old password":"Old password is wrong!"},status=status.HTTP_400_BAD_REQUEST)
        try:
            password_validation.validate_password(
                password= serilaizer.validated_data.get("new_password") , 
                user=user
            )
        except ValidationError as e :
            return Response({"New password":list(e.messages)},status=status.HTTP_400_BAD_REQUEST)
        user.set_password(raw_password=serilaizer.validated_data.get("new_password"))
        user.save()
        return Response({"Message":"Password changed successfully"},status=status.HTTP_200_OK)
    
class ProfileAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(self.queryset,user=self.request.user)
        return obj
    

class TestEmailAPIView(generics.GenericAPIView):

    def get(self,request,*args,**kwargs):
        email_obj = EmailMessage('email/hello.tpl', {'name': "mr matin"}, "root@email.com", to=["matin@email.com"])
        EmailThread(email_obj).start()
        return Response("Email Sent")
    
   

    def get_tokens_for_user(user):
        if not user.is_active:
            raise AuthenticationFailed("User is not active")
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


from django.urls import path
from . import views 
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView


app_name = "api-v1"

urlpatterns = [
    # registration 
    path("registration/",views.RegistrationAPIView.as_view(),name="registration"),
    path("test-email/",views.TestEmailAPIView.as_view(),name="test-email"),

    # change password 
    path("change_password/",views.ChangePasswordApiView.as_view(),name="change_password"),

    #activation 


    # reset password 


    # login token 
    path("token/login/",views.CustomObtainTokenView.as_view(),name="token-login"),
    path("token/logout/",views.CustomDiscardTokenView.as_view(),name="token-logout"),
    # login jwt 
    path("jwt/create/",views.CustomJwtTokenObtainPairView.as_view(),name="jwt-create") , 
    path("jwt/refresh/",TokenRefreshView.as_view(),name="jwt-refresh") , 
    path("jwt/verify/",TokenVerifyView.as_view(),name="jwt-verify"),

    #Profile 
    path("profile/",views.ProfileAPIView.as_view(),name="profile"),

]   
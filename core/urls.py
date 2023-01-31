from django.urls import path
from core.views import (
    SendPasswordResetEmailView,
    UserChangePasswordView, 
    UserLoginView, 
    UserProfileView, 
    UserRegistrationView, 
    UserPasswordResetView,
    CouponsListView,
    CouponsCreateView,
    CouponsDeleteView,
    UserProfileShowView,
    SendOTPView,
    VerifyOTPView,
     ResendOTPView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)



urlpatterns = [
    path('send_otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend_otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/user_profile/', UserProfileShowView.as_view(), name='user_profile'),
    path('coupons/list/', CouponsListView.as_view(), name='coupons_list'),
    path('coupons/delete/', CouponsDeleteView().as_view(), name='coupons_delete'),
    path('coupons/create/', CouponsCreateView.as_view(), name='coupons_create'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
]



# old code


# from django.urls import include, path
# from rest_framework import routers
# from core.views import UserViewSet,CouponViewSet
# from django.urls import path



# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'coupons', CouponViewSet)
# # router.register(r'example', ExampleView)

# urlpatterns = [
#    path('', include(router.urls)),
# ]
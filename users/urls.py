from rest_framework import routers
from .views import UserViewSet
from django.urls import path, include
from .views import VerifyOTP, LoggedInUser

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # path('email/<uuid:token>/', verify_email, name='verify_email'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('verify/otp/', VerifyOTP.as_view(), name='verify_otp'),
    path('user/', LoggedInUser.as_view(), name='logged_in_user')
]

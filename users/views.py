from users.models import User
from django.http import Http404, HttpResponse
from django.db.models import F
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async

from rest_framework import views, response, viewsets, authentication, permissions
from rest_framework.decorators import action

from .serializers import UserSerializer
from .helper import generateOTP, verifyOTP, email_verification_send, filter_dict
from users.permissions import IsCandidate, IsAdmin, IsHr

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAdmin]
        elif self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], permission_classes=[IsAdmin])
    def registerHr(self, *args, **kwargs):
        return super(viewsets.ModelViewSet, self).create(*args, **kwargs)



class LoggedInUser(views.APIView):
    """
    User details of current user
    """

    authentication_classes = [authentication.TokenAuthentication , authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, req, format=None):
        """
        Get user details of current user
        """

        serializer = UserSerializer(req.user)        
        return response.Response(serializer.data)


class VerifyOTP(views.APIView):
    """
    Email/ Phone Number verification through OTP API
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, req, format=None):
        """
        Generates OTP for email/phone_number verification
        """

        field = req.query_params.get('field','')
        digits = int(req.query_params.get('digits', 6))
        valid_for = int(req.query_params.get('valid_for', 120))
        data = req.query_params.get('data')
        otp = generateOTP(data, field, digits, valid_for)

        if(field == 'email'):

            email_verification_send(data, otp)
            return response.Response({
                "valid_for" : valid_for,
                "digits" : digits
            })
        
        elif(field == 'phone_number'):

            return response.Response({
                "otp" : otp,
                "valid_for" : valid_for,
                "digits" : digits
            })

        return response.Response({
            "error" : "Field not found."
        }, 404)

    def post(self, req, format=None):
        """
        Generates OTP for email/phone_number verification
        """

        field = req.query_params.get('field')
        otp = req.data.get('otp')
        data = req.data.get('data')

        if(field == 'email'):
            if verifyOTP(data, field, otp):
                return response.Response()
        
        elif(field == 'phone_number'):
            if verifyOTP(data, field, otp):
                return response.Response()
        else:
            return response.Response({
                "error" : "Field not found."
            }, 404)

        return response.Response({
            "error" : "OTP not valid or OTP has expired."
        }, 404)


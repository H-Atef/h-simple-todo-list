# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import UserSerializer
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import OutstandingToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
import datetime


class RegistrationView(generics.CreateAPIView):
    """
    Handles user registration/signup process by creating a new User.

    """
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # The email check and user creation are handled in the serializer itself
        return super().create(request, *args, **kwargs)
        



class LogOutView(APIView):
    """
    View to log out a user by blacklisting the refresh token.
    
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request):
        """
        Handles POST requests to log out the user by blacklisting the refresh token.
        The refresh token is taken from the cookies and stored in the blacklist.
        
        """

        refresh_token=request.data.get("refresh_token")

        # token=request.auth
        # print(token)
        # print(token.payload['iat'])
        # print(outstanding_token.created_at.timestamp())
        try:

          
            
            # # Retrieve the OutstandingToken instance using the refresh token
            outstanding_token = OutstandingToken.objects.get(token=refresh_token)
            

            # Create a new BlacklistedToken instance using the OutstandingToken
            BlacklistedToken.objects.create(token=outstanding_token)

            outstanding_token.delete()

            


            # Return a success message after blacklisting the refresh token
            return Response({"message": "You have successfully logged out!"}, status=200)
        

        except ObjectDoesNotExist:
            # If the OutstandingToken instance does not exist, handle the error
            raise AuthenticationFailed('Refresh token does not exist in OutstandingToken.')

        except Exception as e:
            # Catch any other errors and return an error message
            raise AuthenticationFailed(f'message : error occurred while logging out process {e}' )




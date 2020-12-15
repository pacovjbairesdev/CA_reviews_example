from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Method for creating a new :model:`core.User` in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Method for creating a new authentication token for
       a :model:`core.User` with credentials"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Viewpoint for checking and updating an authenticated :model:`core.User` profile"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Use the model for the logged user"""
        return self.request.user

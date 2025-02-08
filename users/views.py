from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from users.serializers import UserSerializer


@extend_schema(
    summary='Get current user'
)
class UserMeRetrieveAPIView(generics.RetrieveAPIView):
    """Get info about current user"""

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        return self.request.user

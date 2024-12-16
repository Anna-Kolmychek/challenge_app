from rest_framework import generics, permissions

from users.serializers import UserSerializer


class UserMeRetrieveAPIView(generics.RetrieveAPIView):
    """Get info about current user"""

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        return self.request.user

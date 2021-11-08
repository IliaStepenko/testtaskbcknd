
from rest_framework import status

from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet


from users.permissions import IsOwnerOrAdminPermission
from users.serializers import CurrentUserSerializer, UserSerializer


@api_view(['GET'])
def get_current_user(request):
    if request.user.is_anonymous:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user_data = CurrentUserSerializer(request.user).data
    return Response(user_data)


class UserViewSet(ModelViewSet):
    model = get_user_model()
    serializer_class = UserSerializer
    queryset = model.objects.all()

    def get_permissions(self):

        if self.action == 'create':
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, IsOwnerOrAdminPermission ]

        return super().get_permissions()
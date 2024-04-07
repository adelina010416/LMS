from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from materials.permissions import IsModarator, IsOwner
from users.models import User
from users.serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated & IsModarator]
        else:
            permission_classes = [IsAuthenticated & (IsModarator | IsOwner)]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.data['password'])
        user.save()

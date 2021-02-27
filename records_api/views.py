from rest_framework.response import Response
from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Group, User
from django.views.decorators.cache import cache_page

from records.models import Record
from .serializers import RecordListSerializer, UserSerializer
# Create your views here.


# class RecordsView(viewsets.ViewSet):
#    def list(self, request):
#        queryset = Record.objects.all()
#        serializer = RecordListSerializer(queryset, many=True)
#        return Response(serializer.data)

class UserList(generics.ListAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RecordsView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated,
                         IsAdminUser]
    queryset = Record.objects.all().select_related('category')
    serializer_class = RecordListSerializer

    

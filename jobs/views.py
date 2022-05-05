from .models import Job
from .serializers import JobSerializer

from rest_framework import viewsets, permissions
from users.permissions import IsAdmin

# Create your views here.
class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Jobs to be viewed or edited.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]
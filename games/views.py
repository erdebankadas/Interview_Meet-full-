from .models import Game
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import GameSerializer
from rest_framework.response import Response


class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Game to be viewed or edited.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        name = request.query_params.get('name')
        
        if name :
            queryset = Game.objects.filter(name=name)
        else:
            queryset = Game.objects.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

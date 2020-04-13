import logging

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView
from .models import Match, Player
from .serializers import MatchSerializer 
from balancer.balance.balance import BalanceService

logger = logging.getLogger(__name__)

# Create your views here.
class MatchReadCreate(ListCreateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = MatchSerializer

    def get_queryset(self):
       matchs = Match.objects.all()
       return matchs
    

    def get(self, request):
        matchs = self.get_queryset()
        serializer = self.serializer_class(matchs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Balancer(CreateAPIView): 
    """
    API endpoint for Balance Match

    """
    serializer_class = MatchSerializer

    def get_queryset(self):
       matchs = Match.objects.all()
       return matchs
    

    def get(self, request):
        matchs = self.get_queryset()
        serializer = self.serializer_class(matchs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ Balance un match """
        logger.info('Post Call')
        serializer = self.serializer_class(data=request.data)
        logger.info('serializer')
        if serializer.is_valid():
            balancerService = BalanceService()
            balancerService.run(serializer.validated_data['players'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
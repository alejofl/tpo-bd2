from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class Clients(APIView):
    def get(self, request):
        # TODO
        return Response({"Hello": "World"}, status=status.HTTP_200_OK)
    
    def post(self, request):
        # TODO
        return Response({"Hello": "World"}, status=status.HTTP_201_CREATED)

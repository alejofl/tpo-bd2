import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cliente, Producto
from .persistence import PostgresPersistence, MongoPersistence


persistence = PostgresPersistence() if not eval(os.environ.get("USE_NOSQL")) else MongoPersistence()


class Clients(APIView):
    def get(self, request):
        return Response(persistence.get_clients(), status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        if data.get("nombre") is None or \
           data.get("apellido") is None or \
           data.get("direccion") is None or \
           data.get("activo") is None:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response(persistence.new_client(data.get("nombre"), data.get("apellido"), data.get("direccion"), data.get("activo")), status=status.HTTP_201_CREATED)


class ClientInformation(APIView):
    def get(self, request, id):
        try:
            return Response(persistence.get_client(id), status=status.HTTP_200_OK)
        except Cliente.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            data = request.data
            if len(data) == 0:
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            return Response(persistence.update_client(id, data.get("nombre"), data.get("apellido"), data.get("direccion"), data.get("activo")), status=status.HTTP_200_OK)
        except Cliente.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            return Response(persistence.delete_client(id), status=status.HTTP_200_OK)
        except Cliente.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

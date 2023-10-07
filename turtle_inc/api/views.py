import os
import dotenv
from django.db import DataError
from pymongo import MongoClient
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from turtle_inc import settings
from .models import *
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
        try:
            return Response(persistence.new_client(data.get("nombre"), data.get("apellido"), data.get("direccion"), data.get("activo")), status=status.HTTP_201_CREATED)
        except DataError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
        except DataError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            return Response(persistence.delete_client(id), status=status.HTTP_200_OK)
        except Cliente.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


class Products(APIView):
    def get(self, request):
        return Response(persistence.get_products(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        if data.get("marca") is None or \
           data.get("nombre") is None or \
           data.get("descripcion") is None or \
           data.get("precio") is None or \
           data.get("stock") is None:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        try:
            return Response(persistence.new_product(data.get("marca"), data.get("nombre"), data.get("descripcion"), data.get("precio"), data.get("stock")), status=status.HTTP_201_CREATED)
        except DataError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProductInformation(APIView):
    def get(self, request, id):
        try:
            return Response(persistence.get_product(id), status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            data = request.data
            if len(data) == 0:
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            return Response(persistence.update_product(id, data.get("marca"), data.get("nombre"), data.get("descripcion"), data.get("precio"), data.get("stock")), status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        except DataError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            return Response(persistence.delete_product(id), status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


class MigrationAssistant(APIView):
    def post(self, request):
        print(eval(os.environ.get("USE_NOSQL")))
        if eval(os.environ.get("USE_NOSQL")):
            return Response({"error": "Already migrated to NoSQL"}, status=status.HTTP_400_BAD_REQUEST)

        mongo_client = MongoClient(os.environ.get("MONGO_HOST"), int(os.environ.get("MONGO_PORT")))
        mongo_client.drop_database(os.environ.get("MONGO_DATABASE"))
        db = mongo_client[os.environ.get("MONGO_DATABASE")]
        clients = db["E01_CLIENTE"]
        products = db["E01_PRODUCTO"]
        invoices = db["E01_FACTURA"]

        product_objects = []
        for product in Producto.objects.all():
            product_objects.append({
                "codigo_producto": product.codigo_producto,
                "marca": product.marca,
                "nombre": product.nombre,
                "descripcion": product.descripcion,
                "precio": product.precio,
                "stock": product.stock
            })
        products.insert_many(product_objects)

        for client in Cliente.objects.all():
            telephones = []
            for telephone in client.telefono_set.all():
                telephones.append({
                    "codigo_area": telephone.codigo_area,
                    "nro_telefono": telephone.nro_telefono,
                    "tipo": telephone.tipo
                })
            clients.insert_one({
                "nro_cliente": client.nro_cliente,
                "nombre": client.nombre,
                "apellido": client.apellido,
                "direccion": client.direccion,
                "activo": client.activo,
                "telefonos": telephones
            })

        for invoice in Factura.objects.all():
            details = []
            for detail in invoice.detallefactura_set.all():
                details.append({
                    "id_producto": products.find_one({"codigo_producto": detail.codigo_producto.codigo_producto})["_id"],
                    "nro_item": detail.nro_item,
                    "cantidad": detail.cantidad
                })
            invoices.insert_one({
                "fecha": invoice.fecha.isoformat(),
                "total_sin_iva": invoice.total_sin_iva,
                "total_con_iva": invoice.total_con_iva,
                "iva": invoice.iva,
                "id_cliente": clients.find_one({"nro_cliente": invoice.nro_cliente.nro_cliente})["_id"],
                "detalle_factura": details
            })

        global persistence
        persistence = MongoPersistence()
        os.environ["USE_NOSQL"] = "True"
        dotenv.set_key(os.path.join(settings.BASE_DIR, ".env"), "USE_NOSQL", os.environ["USE_NOSQL"])

        return Response({}, status=status.HTTP_200_OK)

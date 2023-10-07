import os
from abc import ABC, abstractmethod
from bson.objectid import ObjectId
from pymongo import MongoClient
from .models import Cliente, Producto


class PersistenceModule(ABC):
    @abstractmethod
    def get_clients(self):
        pass

    @abstractmethod
    def get_client(self, id):
        pass

    @abstractmethod
    def new_client(self, first_name, last_name, address, active):
        pass

    @abstractmethod
    def update_client(self, id, first_name, last_name, address, active):
        pass

    @abstractmethod
    def delete_client(self, id):
        pass

    def serialize_client(self, id, first_name, last_name, address, active):
        return {
            "nro_cliente": str(id),
            "nombre": first_name,
            "apellido": last_name,
            "direccion": address,
            "activo": str(active)
        }

    @abstractmethod
    def get_products(self):
        pass

    @abstractmethod
    def get_product(self, id):
        pass

    @abstractmethod
    def new_product(self, brand, name, description, price, stock):
        pass

    @abstractmethod
    def update_product(self, id, brand, name, description, price, stock):
        pass

    @abstractmethod
    def delete_product(self, id):
        pass

    def serialize_product(self, id, brand, name, description, price, stock):
        return {
            "codigo_producto": str(id),
            "marca": brand,
            "nombre": name,
            "descripcion": description,
            "precio": str(price),
            "stock": str(stock)
        }


class PostgresPersistence(PersistenceModule):
    def get_clients(self):
        clients = Cliente.objects.all()
        clients_array = []
        for client in clients:
            clients_array.append(self.serialize_client(client.nro_cliente, client.nombre, client.apellido, client.direccion, client.activo))
        return clients_array

    def get_client(self, id):
        client = Cliente.objects.get(nro_cliente=id)
        return self.serialize_client(client.nro_cliente, client.nombre, client.apellido, client.direccion, client.activo)

    def new_client(self, first_name, last_name, address, active):
        client = Cliente(nombre=first_name, apellido=last_name, direccion=address, activo=active)
        client.save()
        return self.serialize_client(client.nro_cliente, client.nombre, client.apellido, client.direccion, client.activo)

    def update_client(self, id, first_name, last_name, address, active):
        client = Cliente.objects.get(nro_cliente=id)
        if first_name is not None:
            client.nombre = first_name 
        if last_name is not None:
            client.apellido = last_name
        if address is not None:
            client.direccion = address
        if active is not None:
            client.activo = active
        client.save()
        return self.serialize_client(client.nro_cliente, client.nombre, client.apellido, client.direccion, client.activo)

    def delete_client(self, id):
        Cliente.objects.get(nro_cliente=id).delete()

    def get_products(self):
        products = Producto.objects.all()
        products_array = []
        for product in products:
            products_array.append(self.serialize_product(product.codigo_producto, product.marca, product.nombre, product.descripcion, product.precio, product.stock))
        return products_array

    def get_product(self, id):
        product = Producto.objects.get(codigo_producto=id)
        return self.serialize_product(product.codigo_producto, product.marca, product.nombre, product.descripcion, product.precio, product.stock)

    def new_product(self, brand, name, description, price, stock):
        product = Producto(marca=brand, nombre=name, descripcion=description, precio=price, stock=stock)
        product.save()
        return self.serialize_product(product.codigo_producto, product.marca, product.nombre, product.descripcion, product.precio, product.stock)

    def update_product(self, id, brand, name, description, price, stock):
        product = Producto.objects.get(codigo_producto=id)
        if brand is not None:
            product.marca = brand
        if name is not None:
            product.nombre = name
        if description is not None:
            product.descripcion = description
        if price is not None:
            product.precio = price
        if stock is not None:
            product.stock = stock
        product.save()
        return self.serialize_product(product.codigo_producto, product.marca, product.nombre, product.descripcion, product.precio, product.stock)

    def delete_product(self, id):
        Producto.objects.get(codigo_producto=id).delete()


class MongoPersistence(PersistenceModule):
    def __init__(self):
        self.client = MongoClient(os.environ.get("MONGO_HOST"), int(os.environ.get("MONGO_PORT")))
        db = self.client[os.environ.get("MONGO_HOST")]
        self.clients = db["E01_CLIENTE"]
        self.products = db["E01_PRODUCTO"]

    def get_clients(self):
        clients = self.clients.find()
        clients_array = []
        for client in clients:
            clients_array.append(self.serialize_client(client["_id"], client["nombre"], client["apellido"], client["direccion"], client["activo"]))
        return clients_array

    def get_client(self, id):
        client = self.clients.find_one({"_id": ObjectId(id)})
        if client is not None:
            return self.serialize_client(client["_id"], client["nombre"], client["apellido"], client["direccion"], client["activo"])
        else:
            raise Cliente.DoesNotExist

    def new_client(self, first_name, last_name, address, active):
        client = self.clients.insert_one({
            "nombre": first_name,
            "apellido": last_name,
            "direccion": address,
            "activo": active
        })
        return self.get_client(str(client.inserted_id))

    def update_client(self, id, first_name, last_name, address, active):
        update_data = {}
        if first_name is not None:
            update_data["nombre"] = first_name 
        if last_name is not None:
            update_data["apellido"] = last_name
        if address is not None:
            update_data["direccion"] = address
        if active is not None:
            update_data["activo"] = active
        update_result = self.clients.update_one({"_id": ObjectId(id)}, update_data)
        if update_result.matched_count > 0:
            return self.get_client(id)
        else:
            raise Cliente.DoesNotExist

    def delete_client(self, id):
        delete_result = self.clients.delete_one({"_id": ObjectId(id)})
        if delete_result.deleted_count == 0:
            raise Cliente.DoesNotExist

    def get_products(self):
        pass

    def get_product(self, id):
        pass

    def new_product(self, brand, name, description, price, stock):
        pass

    def update_product(self, id, brand, name, description, price, stock):
        pass

    def delete_product(self, id):
        pass

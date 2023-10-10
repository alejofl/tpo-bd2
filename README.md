# Turtle Inc.

Turtle Inc. is a simple system that portraits the use of SQL and NoSQL databases for CRUD operations, via a REST API. The purpuse of this project is implement and understand the differences between the resolution of queries in PostgreSQL and MongoDB.

<hr>

* [Prerequisites](#prerequisites)
* [Running Turtle Inc.](#running-turtle-inc)
* [API Endpoints](#api-endpoints)
   * [/clients](#clients)
   * [/clients/&lt;id&gt;](#clientsid)
   * [/products](#products)
   * [/products/&lt;id&gt;](#productsid)
   * [/migration](#migration)
* [Final Remarks](#final-remarks)

<hr>

## Prerequisites

To run the project, you must have the following dependencies in your system.

* Docker
* Docker Compose (Windows and macOS binaries of Docker contain this already, Linux users must install it separately)

## Running Turtle Inc.

Firstly, clone the project and `cd` into the project root directory.

Then, copy the contents of `./turtle_inc/.env.sample` into a new file named `./turtle_inc/.env`. You can use the following shell command, for your convenience:

```bash
cat ./turtle_inc/.env.sample > ./turtle_inc/.env
```

Laslty, start the Docker containers with the following command:

```bash
docker compose up
```
This will download the official PostgreSQL and MongoDB images from Docker Hub, if there aren't already downloaded, and instantiate three containers and a virtual network, for these containers to communicate internally. All of this boilerplate is done automatically.

To stop the application but maintain the volumes and data associated with it, run the following:

```bash
docker compose down
```

If you wish to stop the application and remove all of the related data, run the following:

```bash
docker compose down --rmi local -v
```

**After starting the application, the API will be accesible at `localhost:8000`**

## API Endpoints

The REST API, written using Django REST Framework, can be accesed using any HTTP request service as cURL, Postman, Insomnia, among others. Django also creates a visual interface for the API to be used via the browser. The following endponts available to make CRUD operations:

### `/clients`

* GET request: retrieves an array of all the clients registered in the database.

* POST request: creates a new client in the database. The body of the request must contain the following JSON object.

```json
{
    "nro_cliente": "",
    "nombre": "",
    "apellido": "",
    "direccion": "",
    "activo": ""
}
```

### `/clients/<id>`

* GET request: retrieves the client whose id is `<id>`.

* PUT request: updates the client whose id is `<id>`, updating the fields specified in the body, which must contain any of the fields from the POST request to `/clients`.

* DELETE request: deletes the client whose id is `<id>`.

### `/products`

* GET request: retrieves an array of all the products registered in the database.

* POST request: creates a new product in the database. The body of the request must contain the following JSON object.

```json
{
    "codigo_producto": "",
    "marca": "",
    "nombre": "",
    "descripcion": "",
    "precio": "",
    "stock": ""
}
```

### `/products/<id>`

* GET request: retrieves the product whose id is `<id>`.

* PUT request: updates the product whose id is `<id>`, updating the fields specified in the body, which must contain any of the fields from the POST request to `/products`.

* DELETE request: deletes the product whose id is `<id>`.

### `/migration`

Via this endpoint, the user may make the migration from PostgreSQL to MongoDB. All of the contents of the relational database will be added to the NoSQL database.

This endpoint also updates the `.env` file, changing the variable `USE_NOSQL` to `True`. This means that, from now on, all of the CRUD operations will be made over the MongoDB database. You can change this behaviour by updating the variable inside the `.env` file and restarting the application.

## Final Remarks

This project was done in an academic environment, as part of the curriculum of Databases II from Instituto Tecnológico de Buenos Aires (ITBA)

The project was carried out by:

* [Alejo Flores Lucey](https://github.com/alejofl/)
* [Andrés Carro Wetzel](https://github.com/AndresCarro/)
* [Camila Di Toro](https://github.com/camilaDiToro/)
* [Nehuén Gabriel Llanos](https://github.com/NehuenLlanos/)

# tpo-bd2

First, `cd` into `./turtle_inc` and create a `.env` file, with the same contents as `.env.sample`

Then, on the root folder of the project, run
```bash
docker compose up
```

This will start the postgres and mongo databases as well as the django app, currently using a sqlite database. 

After starting the docker containers you can verify that django is running in the port 8000.

Then, by running 

```bash
psql -h 172.17.0.1 -p 5432 -U postgres
```
You will be able to connect to the postgres database. The password is postgres. 

Inside the psql command line, run

```postgresql
SELECT * FROM numbers;
```
 just if you want to verify that the sql initial script was loaded (the numbers table should exist and be empty).
 
The same way, the connection to the mongo database can be checked:

```bash
mongosh mongodb://172.17.0.1:27017
```
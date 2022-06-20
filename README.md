# The final project of the NIX training program.

## Application on the FLASK framework, movie site.

### General command:

* Build app.
* ``` docker-compose --env-file .env up --build``` or ```make build```
* Start app (no logs)
* ``` docker-compose --env-file .env up -d``` or ```make up```
* Stop App
* ``` docker-compose down``` or ```make down```
* Work inside container web.
* ``` docker exec -it web_app bash``` or ``` make exec ```
* ADD First data(Role/genre/director)
* ```python project/database/db_add.py``` or ``` make add ```
* Add Admin user.
* ```python project/database/db_add_admin.py``` or ```make admin```
* Seed site data.
* ```python project/database/db_seed.py``` or ```make seed```
* Run test.
* ```pytest``` or ```make test```
* Del all image docker:
* ```docker rm -f $(docker ps -a -q)``` or ```make rm```

Url with swagger documentation — http://localhost/swagger


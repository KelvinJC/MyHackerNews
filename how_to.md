### Transfer app data from SQLITE to POSTGRES 
1. Download and install postgres from this link [https://www.postgresql.org/download/windows/] 

2. Run the following command while sqlite3 is still the operational database.

```
python -Xutf8 ./manage.py dumpdata > data.json
```

**OR**


* You can also use the modified version of the above command by including natural primary & foreign keys as follows:

```
python manage.py dumpdata — natural-foreign — natural-primary > whole.json
```

* It will generate the SQLite dump data in the JSON fixture format. 
* It is suggested that you use this alternate command only if you face any error in restoring(loaddata) data to PostgreSQL

<br><br>

3. Create the postgres database

4. Install the psycopg2 package. It is a SQL DB-API that acts as a driver between the Django ORM and a Postgres database instance.

```
pip install psycopg2
```

5. Configure the settings.py file by replacing the Databases parameter. <br>

* For example: <br>


DATABASES = {
‘default’: {
‘ENGINE’: ‘django.db.backends.postgresql_psycopg2’,
‘NAME’: ‘new_db’,
‘USER’ : ‘john’,
‘PASSWORD’ : ‘new_db@123’,
‘HOST’ : ‘localhost’,
‘PORT’ : ‘5452’,
}
}

#### NOTE:
#### REMEMBER TO USE ENVIRONMENT VARIABLES TO PROTECT CREDENTIALS
<br><br>


6. Delete the content types(mandatory steps) to avoid numerous errors as follows:

```
python manage.py shell
```

* Within the shell enter and run the following lines

```
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
```
* Exit the shell
<br><br>


7. Within the migrations directory of each app that has been created, delete all old migrations files and the  '__pycache__' file.

8. Create new migrations and migrate the models by running the following commands in succession.

```
python manage.py makemigrations
python manage.py migrate
```
<br><br>


9. Import Required Fixture via Loaddata from SQLite to PostgreSQL

```
python manage.py loaddata data.json
```

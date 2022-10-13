# MyHackerNews

## News Aggregation Web Application

MyHackerNews is a simple application that allows users to register and log into a web client, get a constantly fresh and up to date 
feed of tech related news articles and tech job posts.


Within the project, the three apps worthy of note are:
1. News - Sourcing, display and addition of news articles  
2. Jobs - Sourcing, display and addition of jobs articles  
3. Accounts - Handles user authentication and authorisation

### Prerequisite
1. As this is a Django application you will need to have Python installed on your system. You can download and install Python from 
[https://www.python.org/downloads/). This will allow you to be able to run 'python' commands.


## Getting Started
* Create a new directory where you would like this project stored. e.g NewsApp

* Change into that new directory

```
cd NewsApp
```

* Get a copy of the source code of this project into your local repository.

```
git clone https://github.com/KelvinJC/MyHackerNews.git
```

* The code will be packaged in a directory named MyHackerNews so change into that directory

```
cd MyHackerNews
```

<br><br>
* *In accordance with best practices, run this project within a virtual environment.*<br>
<br><br>

* Create a virtual environment. (Windows OS. Check out how to create and activate a virtual environment if you are on a different OS.)

```
python -m venv <name_of_environment> 
```

* Activate that environment

```
source venv/Scripts/activate 
```

* Install project dependencies

```
pip install django
pip install requests
```


### Database Creation

This project makes use of a sqlite database for storage of articles and job posts as well as user information. If you require a different database, customisation is possible via the settings.py file. <br>
For the sake of simplicity however, we will focus on using sqlite3. <br><br>


Change into the source code directory

```
cd src 
```

Run the following commands in succession

```
python manage.py makemigrations
python manage.py migrate
```


### Create a Django Admin User
This step is not critical to the usage of the app but if you are familiar with the Django Admin UI you can create a superuser i.e Admin

```
python manage.py createsuperuser 
```

Following the prompts you may enter your details for username, e-mail address (optional), password, password re-entry. <br><br>



### Run server:

To begin using the application. Initiate the server by running the following command

``` 
python manage.py runserver 
```

By default, Django apps listen on http://127.0.0.1:8000 so once the server is running, that is the link to copy and paste into your preferred browser






## Tips
1. Take a look at `udagram-api` -- does it look like we can divide it into two modules to be deployed as separate microservices?
2. The `.dockerignore` file is included for your convenience to not copy `node_modules`. Copying this over into a Docker container might cause issues if your local environment is a different operating system than the Docker image (ex. Windows or MacOS vs. Linux).
3. It's useful to "lint" your code so that changes in the codebase adhere to a coding standard. This helps alleviate issues when developers use different styles of coding. `eslint` has been set up for TypeScript in the codebase for you. To lint your code, run the following:
    ```bash
    npx eslint --ext .js,.ts src/
    ```
    To have your code fixed automatically, run
    ```bash
    npx eslint --ext .js,.ts src/ --fix
    ```
4. `set_env.sh` is really for your backend application. Frontend applications have a different notion of how to store configurations. Configurations for the application endpoints can be configured inside of the `environments/environment.*ts` files.
5. In `set_env.sh`, environment variables are set with `export $VAR=value`. Setting it this way is not permanent; every time you open a new terminal, you will have to run `set_env.sh` to reconfigure your environment variables. To verify if your environment variable is set, you can check the variable with a command like `echo $POSTGRES_USERNAME`.

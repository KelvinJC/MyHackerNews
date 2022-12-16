# MyHackerNews

## News Aggregation Web Application

MyHackerNews is a simple application that allows users to get up to date on tech-related news articles and tech job posts. Registered users can contibute by adding links to their blogs and online articles.


Within the project, the three apps worthy of note are:
1. News - Sourcing, display and addition of news articles  
2. Jobs - Sourcing, display and addition of jobs articles  
3. Accounts - Handles user authentication and authorisation

### Prerequisite
1. As this is a Django application you will need to have Python installed on your system. You can download and install Python from 
[https://www.python.org/downloads/]. This will allow you to be able to run 'python' commands.


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


### Credentials management
It is a good idea to store credentials as environment variables so within the src directory create a .env file and insert your application's credentials.


Change into the source code directory

```
cd src 
```

Create a .env file and copy the into it the following:

SECRET_KEY=your secret key (found in the settings.py file) <br>
DEBUG=1 <br>
ALLOWED_HOST=127.0.0.1  


### Database Creation

This project makes use of a PostgreSQL database. You can install a postgres locally visit here. 

Put all database credentials in the .env file created earlier

DATABASE_NAME=your_database_name <br>
DATABASE_USER=your_database_user <br>
DATABASE_PASSWORD=your_database_password <br>
DATABASE_HOST=your_database_host <br>
DATABASE_PORT=your_database_port_number

Make sure you are in the src/ directory

Run the following commands in succession

```
python manage.py makemigrations
python manage.py migrate
```

NB.<br>
To learn how to transfer transfer data from sqlite to postgres, click on this [link.](how_to.md)

### Create a Django Admin User
This step is not critical to the usage of the app but if you are familiar with the Django Admin UI you can create a superuser i.e Admin

```
python manage.py createsuperuser 
```

Following the prompts you may enter your details for username, e-mail address (optional), password, password re-entry. <br><br>



### Run the server:

To begin using the application. Initiate the server by running the following command

``` 
python manage.py runserver 
```

By default, all Django applications listen on http://127.0.0.1:8000 so once the server is running, copy and paste the link into your preferred browser.



## Screenshots
* Home page
![](zreadme_imgs/Screenshot (160).png)
<br><br>

* News stories
![](zreadme_imgs/news.png)
<br><br>

* Jobs stories
![](zreadme_imgs/jobs.png)


## User Tips
1. Click on the refresh dropdown and then refresh news stories or refresh job stories to update your feed.
2. Sign in to be able to create news and job stories.
3. To search for news and job articles by poster, link or article title, use the search bar in the navbar area or on the respective pages.

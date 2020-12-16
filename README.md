# CA_reviews_example

# Local setup

Install the following: 

+ Docker https://www.docker.com/
+ Git client https://desktop.github.com/


# App setup

+ Clone https://github.com/pacovjbairesdev/CA_reviews_example.git
+ Go to CA_reviews_example folder in a Shell
+ Execute 
	* > docker build .
	* > docker-compose build
	* > docker-compose up
+ You can either check the API in a browser or by sending CURL requests


# API structure

* /api/user/create/ POST new users
* /api/user/token/ POST for an AuthToken
* /api/user/me/ Viewpoint for GET, PUT and PATCH user data
* /api/review/reviews/ Viewpoint for GET a list of all the user' reviews and POST new reviews


# Chrome considerations

ModHeader extension will allow you to easy set up the "Authorization" request header needed for the review viewpoint.


# User model features

	- id (read-only)
	- email
	- name
	- password (write-only a.k.a. cant be view from GET requests only editable from POST)


# Review model features
	
	- id (read-only)
	- title 
	- rating
	- summary
	- company
	- ip (read-only)
	- submission_date (read-only)
	- reviewer (read-only foreign key to User that submitted the review)


# Steps to follow for a quick tour

+ Create a user in http://127.0.0.1:8000/api/user/create/
+ Get the authentication token in http://127.0.0.1:8000/api/user/token/
+ Set the "Authorization" request header to "Token <value>" e.g. "Token 923b699f44111bf09f2877c2fe65172d1e595549". 
	- Every user has its own token.
	- The token tells the API the user that is accessing.
+ Access to http://127.0.0.1:8000/api/review/reviews/
	- Use a GET request for listing all the reviews.
	- Use a POST request for creating a new one. Must specify all the non read-only fields.
+ Access to http://127.0.0.1:8000/api/user/me/ to:
	- GET the authenticated user profile.
	- PATCH an update to a non read-only field.
	- PUT an update to the User profile.


# Code structure

+ /  Contains all the setup files for GitHub, Docker, Docker Compose and Python.
	+ /app  Contains the code of the application.
		+ /app  Contains the main settings of the API.
		+ /core  Contains the models and the django-admin configuration.
			+ /management/commands  Contains a command for ensuring db sync.
			+ /tests  Contains unit tests for the management command and for the models.
		+ /user  Contains the views, urls and serializers for the tasks related to the User model.
			+ /tests  Contains unit tests for validating all the User model endpoints (hosted in /api/user/) with authenticated and non-authenticated users.
		+ /review  Contains the views, urls and serializers for the tasks related to the Review model.
			+ /tests  Contains unit tests for validating all the Review model endpoints (hosted in /api/review/) with authenticated and non-authenticated users.


# Testing

+ Go to CA_reviews_example folder in a Shell
+ Execute 
	> docker-compose run --rm app sh -c "python manage.py test && flake8"
+ Check the test results


# Test summary

There is a total of 24 tests
+ 8 tests for using/restricting user viewpoint functions with a non-authenticated user.
+ 3 tests for using/restricting user viewpoint functions with an authenticated user.
+ 1 test for using/restricting review viewpoint functions with a non-authenticated user.
+ 6 tests for using/restricting review viewpoint functions with a non-authenticated user.
+ 1 test for checking the db sync command.
+ 5 test for checking model existence and validation capabilities.


# Django admin

Django admin is configured to give you complete control of:

+ Users
+ Reviews
+ Authentication tokens

It also gives you access to the project docs.


# Creating a superuser for accessing the django admin view

+ Go to CA_reviews_example folder in a Shell
+ Execute 
	> docker-compose run --rm app sh -c "python manage.py createsuperuser"
+ Specify email and password


# Admin structure
 
+ http://127.0.0.1:8000/admin/  Django admin interface
+ http://127.0.0.1:8000/admin/doc/  Django docs

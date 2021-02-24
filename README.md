# Parks Pass
## Frontend Repository
https://github.com/taylorschmidt/Parks-Pass-FrontEnd
## Deployed API
https://parkspassport-api-heroku.herokuapp.com/
## Technology
* Python
* Flask
* Peewee
* PostgreSQL
## General Approach
* Construct models and their class components required for application function.
* Develop RESTful routes that allow for appropriate resource functions to be utilized.
* Write resource functions that allow for proper manipulation of database models.
## Installation Instructions
* Fork and clone repo
* npm -i
## Routes
|ROUTE |CRUD  |URL           |DESCRIPTION                          |
|------|------|--------------|-------------------------------------|
|POST  |Create|“/api/v1/user/register |Register user with API.     |
|POST   |Create  |"/api/v1/user/login”|Login an existing user with API.|
|GET   |Read  |“/api/v1/user/logout|Logout user from API.     |
|GET  |Read|“/api/v1/user/”|Show user data that correlates with a specific email.|
|PUT  |Update|“/api/v1/user/update"|User can update their username.|
|POST   |Create|“/api/v1/person_park”|User can stamp a specific national park to their passport.|
|GET|Update|“/api/v1/person_park/visited|User can retrieved their visited parks from their passport.|
|DELETE|Destroy|“/api/v1/person_park/visited/delete”    |User can remove a visited national park from their passport.|
|POST|Create|“/api/v1/park/”    |A park's information is added to the database.|

## Challenges
* Authorization using flask-login and storing user session data.
* Becoming familiar with python syntax.
* Troubleshooting frontend API calls when backend routes were functioning.
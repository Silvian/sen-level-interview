# Context senior-level interview exercise

This repository contains the skeleton Django `servers` application that you have been asked to complete.
Below is a description of the problem, and what features you need to implement.

While completing this exercise please be aware that your use of `git` is examined as well as your 
code, so please ensure your history is clean and commit messages are clear and meaningful.
**Please submit your code as a Github fork, or in a format that contains the `.git` directory**.

You may also use any external packages if you feel the need.

**Timing:** We expect this task to take between 2 to 4 hours. It does not have to be fully complete 
to be submitted, and will form part of the discussion in your final interview. Please implement as 
much as you can, but do not feel you have to spend excessive amounts of time working out every minor detail.
Adding comments describing any limitations or mostly-complete portions of the functionality is acceptable.

## Server monitoring

Context has a lot of servers, and successful logins to them are logged to a central service. This 
service outputs the **last successful login for each user on the server**, a sample of which can be [found in 
data/logins.csv](data/logins.csv).

The task is to create a view where someone may upload this CSV file. The file
should then be processed and the results stored in a database, 
which you will need to model. A brief overview of the file is given below.

**Bonus points:** Process the CSV file asynchronously.

As well as the upload you must implement a single view that, for each server, displays the 
name and IP, a list of users who have logged in, the time they logged in, and any 
contact information stored for the users.

This view does not need to be pretty (no CSS is required, just plain HTML), but it does need to use as few 
database queries as possible.

### logins.csv

The logins.CSV is a snapshot of the output of the hypothetical central login service. Unfortunately the
CSV file contains some abnormalities that you need to clean up while processing, which are described below.

The following headers are present in the CSV file:

`server-name,server-ip,username,full-name,contact,login-time`

An example row would be:

`foster-chapman,3.82.209.138,amiller,Alex Taylor,+44(0)0705 97317,2017-06-19`

The `server-name` and/or `contact` column is sometimes missing from rows in the output. You can 
choose to ignore these rows, or attempt to fill in the missing information, as long as you justify 
your choice.

Each login has an individual row in the CSV. **However**, if the user that has logged in has multiple 
items of contact information associated with their account, then there will be multiple rows per login.

For example, "Alex Taylor" has an email address and a phone number. Therefore, a single login attempt 
will have two lines in the CSV file:

```
foster-chapman,3.82.209.138,amiller,Alex Taylor,+44(0)0705 97317,2017-06-19
foster-chapman,3.82.209.138,amiller,Alex Taylor,alex@test.com,2017-06-19
```

The Django application should treat multiple lines like this as a single login attempt. At a minimum, the 
system should store one piece of contact information per user. 

**Bonus points:** If users have multiple contacts, store all values that the CSV provides.

#### Docker

The Context dev team uses Docker and docker-compose across all projects.
Submit your project with a docker-compose.yml file, such that we can start
your project using `docker-compose up`. You are free to use images from Docker
Hub, or write your own Dockerfiles.

#### Dates

The output has inconsistent data in the `login-time` column. It could be a standard ISO formatted 
date time, an ISO formatted date or a random python `strftime` formatted string containing the day, month 
and year joined by `/`, `\` or `|`. For example:

```
12\10\2016
10|12|2016
2016/10/12
```

Best-attempt parsing of these ambiguous dates is acceptable, it does not have to be foolproof.

### Testing

Please include some tests in the `monitoring` application where you feel they are appropriate.
To run the application test pack suite within docker container simply run:
#### docker-compose run --rm web python manage.py test

### Installation Guide:

This project is dockerized so the following guide will highlight the requirements and steps needed
to run in a docker environment.

1. Install docker and docker-compose specific to your operating system. See https://www.docker.com for more details.

2. git clone the project and in the project base directory create a .env file with the following inside:

`DATABASE_HOST=postgres`

`DATABASE_NAME=postgres`

`DATABASE_USER=postgres`

`DATABASE_PASSWORD=postgres`

`RABBITMQ_DEFAULT_USER=admin`

`RABBITMQ_DEFAULT_PASS=mypass`

`CELERY_BROKER_URL=amqp://admin:mypass@rabbitmq`

Also don't forget to create a /static/media/upload folder in project base.

3. Inside the project base directory where docker-compose.yml file can be found, run the following commands:
#### docker-compose up --build

4. Once the process has finished and the postgres sql database and application are running,
run the migrations and load data command inside docker as following:
#### docker-compose run --rm web cli/migrate_loaddata.sh

5. This also creates a default user: root with password: root

6. Login to the django administration page at: http://localhost:8000/admin/ with the credentials above to verify this.

*Note:* you can login with the default user created here or create other users via django admin panel.


### Assumptions:

1. From analysing the created data file I have assumed that ```server-ip, username, full-name and login-time```
are mandatory fields. Therefore a unique entry is composed of these 4 fields together.

2. Created two separate fields for contact; one for number and one for email. The reason being, this is quite useful if
we need to email the user automatically. We would want to know that we have a dedicated email field even if nullable.

3. Invalid dates such as 17/19/06 do not make sense in any date format and will be defaulted to unix start time.

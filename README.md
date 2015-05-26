# Wishapp
Waffle board status: [![Ready](https://badge.waffle.io/jykntr/wishapp.svg?label=ready&title=Ready)](http://waffle.io/jykntr/wishapp) [![In Progress](https://badge.waffle.io/jykntr/wishapp.svg?label=in+progress&title=In+Progress)](http://waffle.io/jykntr/wishapp)

## About 

A basic Wishlist application that allows users to create wish lists and others
to reserve the right to purchase those items for the user.

## Customizing

### Configuration

Update the ```config.py``` file with your mail server information.

For convenience, a ```.env``` file can be populated with values for environment
variables.  These environment variables will be set before the application
starts.  An example ```.env``` file for development might look like this:

```
FLASK_CONFIG=development
MAIL_USERNAME=username@example.xom
MAIL_PASSWORD=password
SSL_DISABLE=true
```

## Heroku Support 

### Initial Heroku setup 

You must first create an account on [Heroku](http://heroku.com) if you don't 
already have one, and then install the [Heroku Toolbelt](https://toolbelt.heroku.com)

* Log into Heroku:

 ```
 $ heroku login
 Enter your Heroku credentials.
 Email: ...
 Password (typing will be hidden):
 Authentication successful.
 ```

* Create an application:

 ```
 $ heroku create <custom_app_name>
 Creating <custom_app_name>... done, stack is cedar
 http://<custom_app_name>.herokuapp.com/ | git@heroku.com:<custom_app_name>.git
 Git remote heroku added
 ```

* Create a databse for your application:

 ```
 $ heroku addons:add heroku-postgresql:dev
 Adding heroku-postgresql:dev on <custom_app_name>... done, v3 (free)
 Attached as HEROKU_POSTGRESQL_RED_URL
 Database has been created and is available
 ! This database is empty. If upgrading, you can transfer
 ! data from another database with pgbackups:restore.
 Use `heroku addons:docs heroku-postgresql:dev` to view documentation.
 ```

 Promote the database, it's URL will be exposed in an environment variable 
 named ```DATABASE_URL``` that will be picked up by the application.

 ```
 $ heroku pg:promote HEROKU_POSTGRESQL_RED_URL 
 ```

* Setup Heroku environment:

 Set the required environment variables on the Heroku server.  Start the the 
 ```FLASK_CONFIG``` variable which indicates which configuration the 
 application should use.

 ```
 $ heroku config:set FLASK_CONFIG=heroku
 Setting config vars and restarting <custom_app_name>... done, v4
 FLASK_CONFIG: heroku
 ```

 Next add your mail server information.

 ```
 $ heroku config:set MAIL_USERNAME=<your-gmail-username>
 $ heroku config:set MAIL_PASSWORD=<your-gmail-password>
 ```

### Deploying and/or upgrading your application to Heroku

Optionally move your application into maintenance mode.  This will make Heroku
show users a static page indicating the application is down for maintenance.
Then push your application to Heroku, run the ```deploy``` command and restart
the application.

```
$ heroku maintenance:on  # Turn maintenance mode on
$ git push heroku master  # Deploys your application to Heroku
$ heroku run python manage.py deploy  # sets things up such as the database
$ heroku restart
$ heroku maintenance:off  # Turns off maintenance mode
```

### Testing your Heroku config locally

The [Heroku Toolbelt](https://toolbelt.heroku.com) installs a command named
```foreman``` which can be used to test in an environment more similar to
Heroku. ```foreman``` can set the environment variables normally found on the
Heroku server by reading them from a file named ```.env``` in the root
directory.   Create a ```.env``` file that looks similar to the following:

```
FLASK_CONFIG=heroku
MAIL_USERNAME=<your-username>
MAIL_PASSWORD=<your-password>
SSL_DIASABLE=true
```

The ```foreman``` command can run any arbitrary command in a Heroku-like
environment.  It can be used for things such as testing the ```deploy```
command:

```
$ foreman run python manage.py deploy
```

To test starting the server like it will be started on Heroku run the 
following:

```
$ foreman start
22:55:08 web.1 | started with pid 4246
22:55:08 web.1 | 2013-12-03 22:55:08 [4249] [INFO] Starting gunicorn 18.0
22:55:08 web.1 | 2013-12-03 22:55:08 [4249] [INFO] Listening at: http://...
22:55:08 web.1 | 2013-12-03 22:55:08 [4249] [INFO] Using worker: sync
22:55:08 web.1 | 2013-12-03 22:55:08 [4254] [INFO] Booting worker with pid: 4254
```

### Viewing Heroku logs

Logging is captured by Heroku.  To view the log statements run ```$ heroku
log``` or to tail the logs ```$ heroku log -t```.

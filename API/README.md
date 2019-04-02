# Attendance Manager API
The attendance manager API for Python 3.7 and Amazon AWS Elastic Beanstalk.

MIT License

**NOTE:** I highly recommend using [PyCharm](https://www.jetbrains.com/pycharm/) to configure your environment. It is free for university students. PyCharm lets you easily manage virtual environments, set environment variables, and manage version control.

## Installation

Clone the Git repository into your folder of choice. Navigate to that folder in your terminal. If you are using a virtual environment, make sure you are in that environment. Then, run the following commands in your terminal:
```
pip install --upgrade pip

pip install -r requirements

pi
```

You've just installed [Flask](http://flask.pocoo.org/), [Flask-Migrate](https://flask-migrate.readthedocs.io/), and other important tools!

Next, navigate to the `app` folder (containing `Docs`, `Endpoints`, `Models`, etc) and run the following commands:
```
flask db init
flask db migrate
flask db upgrade
```

Those commands just:
1. Created a `migrations` folder
2. Created your first migrations from the models in the `Models` folder
3. Ran your migrations to create the required database/tables/columns.

Finally, navigate back to the base `API` folder and run `main.py`. Voila!

## Usage

To deploy your application to Elastic Beanstalk (EBS), run `createZIP.sh`.

Example (in terminal):
```
./createZIP.sh production 1_0
```

This generates a file called `1_0.zip` that you can upload to your EBS environment.


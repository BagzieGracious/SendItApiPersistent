[![Build Status](https://travis-ci.org/BagzieGracious/SendItApiPersistent.svg?branch=develop)](https://travis-ci.org/BagzieGracious/SendItApiPersistent)     [![Coverage Status](https://coveralls.io/repos/github/BagzieGracious/SendItApiPersistent/badge.svg?branch=develop)](https://coveralls.io/github/BagzieGracious/SendItApiPersistent?branch=develop)       [![Maintainability](https://api.codeclimate.com/v1/badges/17dfb979a42be3f63ddf/maintainability)](https://codeclimate.com/github/BagzieGracious/SendItApiPersistent/maintainability)


# SendItApi
SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories. This application is a python ([Python 3.6.5](https://docs.python.org/3/)) web api that works or uses flask framework ([Flask](http://flask.pocoo.org/)) technlogy.

# Application Features
* Users can create an account and log in.
* Users can create a parcel delivery order.
* Users can change the destination of a parcel delivery order.
* Users can cancel a parcel delivery order.
* Users can see the details of a delivery order.
* Admin can change the status and present location of a parcel delivery order
* Admin can change the status of a parcel delivery order.
* Admin can change the present location of a parcel delivery order


# Application Endpoints :
 Use the following endpoints to perform the specified tasks 
    
    EndPoint                                     | Functionality
    ------------------------                     | ----------------------
    Get /parcels/                                | Fetch all parcel delivery orders
    Get /parcels/<int:parcel_id>                 | Fetch a specific parcel delivery order
    POST /users/<int:user_id>/parcels            | Fetch all parcel delivery orders by a specific user
    PUT /parcels/<int:parcel_id>/cancel/         | Cancel the specific parcel delivery order
    POST /parcels/                               | Create a parcel delivery order
    PUT /parcels/<int:parcel_id>/destinations    | Change the location of a specific parcel delivery order
    PUT /parcels/<int:parcel_id>/status          | Change the status of a specific parcel delivery order
    PUT /parcels/<int:parcel_id>/presentLocation | Change the present location of a specific parcel delivery order

# Installation

Create a new directory and initialize git in it. Clone this repository by running
```sh
$ git clone https://github.com/BagzieGracious/SendItApiPersistent.git
```

Create a virtual environment. For example, with virtualenv, create a virtual environment named venv using
```sh
$ virtualenv venv
```

Activate the virtual environment
```sh
$ cd venv/scripts/activate
```

Install the dependencies in the requirements.txt file using pip
```sh
$ pip install -r requirements.txt
```

Start the application by running
```sh
$ python run.py
```

Test this end point py running
```sh
$ pytest test_view.py
```

Heroku link
```sh
https://bagzie-send-it-persitent.herokuapp.com
```
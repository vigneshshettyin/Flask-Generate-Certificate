## Running the code the conventional way

Clone this repository to your local drive
 ```shell
$ git clone https://github.com/vigneshshettyin/Flask-Generate-Certificate.git
```

**2.** Change directory into the cloned repository  
 ```shell
$ cd Flask-Generate-Certificate
```

**3.** Setup virtual environment
 ```shell
$ py -m venv env
$ .\env\Scripts\activate
```

**4.** Install requirements from requirements.txt  
 ```shell
$ pip3 install -r requirements.txt
```

**5.** Setup Database

* To initialise a new database
  ```
    python manage.py db init
  ```
* To migrate changes in the database
  ```
  python manage.py db migrate
  ```
* To update the database with the new migrations
  ```
  python manage.py db upgrade
  ```
* To degrade the database
  ```
  python manage.py db downgrade
  ```
**Note** : Users need to run the upgrade command only during the project setup since the initial migrations have already been done. It just need to be applied using the `python manage.py db upgrade` command.

**6.** Run the development server
```shell
$ flask run
```

Now open Google Chrome/IE6/Edge/Firefox browser and go to http://127.0.0.1:5000/
You will find the application running there.

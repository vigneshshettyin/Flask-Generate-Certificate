## Running the code the conventional way

**1.** Clone the forked repository to your local drive
 ```shell
git clone https://github.com/<YOUR_Username>/Flask-Generate-Certificate.git
```

**2.** Change directory into the cloned repository  
 ```shell
cd Flask-Generate-Certificate
```

**3.** Setup virtual environment
 
 **3.1** For Windows
  ```shell
  py -m venv env
  .\env\Scripts\activate
  ```
  **3.2** For Linux
  ```shell
  pip install virtualenv
  ```
  ```shell
  virtualenv your_name
  ```
  ```shell
  virtualenv -p /usr/bin/python3 your_name
  ```

**4.** Install requirements from requirements.txt (While installing if you get any error regarding the boto3, botocore, simply remove the specified versions from both and do not disturb the other.)
 ```shell
pip3 install -r requirements.txt
```

**5.** Create a new file called `.env` and copy all the data from `.env.sample` to `.env` as it is.

**6.** Setup Database

* To initialise a new database
  ```
  flask db init
  ```
* To migrate changes in the database
  ```
  flask db migrate
  ```
* To update the database with the new migrations
  ```
  flask db upgrade
  ```
* To degrade the database
  ```
  flask db downgrade
  ```
**Note** : Users need to run the upgrade command only during the project setup since the initial migrations have already been done. It just need to be applied using the `python manage.py db upgrade` command.

**7.** Run the development server
```shell
flask run
```

Now open Google Chrome/IE6/Edge/Firefox browser and go to http://127.0.0.1:5000/
You will find the application running there.

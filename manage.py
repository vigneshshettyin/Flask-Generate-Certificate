import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import json

with open('import.json', 'r') as c:
    env_var = json.load(c)["jsondata"]

from app import app, db


app.config.from_object(env_var["app_settings"])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

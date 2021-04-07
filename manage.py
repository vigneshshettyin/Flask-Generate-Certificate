import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from decouple import config

from app import app, db


app.config.from_object(config("app_settings"))

if db.engine.url.drivername == 'sqlite':
    migrate = Migrate(app, db, render_as_batch=True)
else:
    migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

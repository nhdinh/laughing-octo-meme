# manager.py

from flask_script import Manager

from app.app_factory import create_app
from flask_migrate import Migrate, MigrateCommand
from app.__common import DbInstance

application = create_app('development')

db = DbInstance.get()
migrate = Migrate(application, db)

manager = Manager(application)
manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    application.run(debug=False)
    return


if __name__ == '__main__':
    manager.run()

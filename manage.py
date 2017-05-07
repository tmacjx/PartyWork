#!/usr/bin/env python
import os
from app import create_app, db

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app.models import Role, User, CurrentNews, WorkTrends, Activity, PartyMember, LearnContent

# os.environ['MODE'] = 'test'

# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
from app import app

# app = create_app()

manager = Manager(app)

migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, CurrentNews=CurrentNews, WorkTrends=WorkTrends,
                Activity=Activity, PartyMembe=PartyMember, LearnContent=LearnContent)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()



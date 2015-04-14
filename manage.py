#!/usr/bin/env python
import sys
import os
from app import create_app, db
from app.models import User, Role
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    print('Unit tests:')
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
    return result.wasSuccessful()


@manager.command
def flake8():
    """Run flake8 tests"""
    from subprocess import call
    print('flake8 checking:')
    retval = call(['flake8',
                   '.',
                   '--exclude=.git,__pycache__,migrations',
                   '--show-source',
                   '--verbose'])
    if retval is 0:
        return True
    else:
        return False


@manager.command
def piprot():
    """Run piprot"""
    from subprocess import call
    print('piprot checking:')
    retval = call(['piprot', 'requirements.txt'])
    if retval is 0:
        return True
    else:
        return False


@manager.command
def build(coverage=False):
    """Run all tests for the full build."""
    passing = True
    passing = passing & test(coverage)
    print('')
    passing = passing & flake8()
    print('')
    piprot()  # Don't fail build because of old requirements.txt

    if not passing:
        sys.exit(1)


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    from app.models import Role

    # migrate database to latest revision
    upgrade()

    # create user roles
    Role.insert_roles()


if __name__ == '__main__':
    manager.run()

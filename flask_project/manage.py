"""
Module in which the manager for the Flask application is initialized.
"""
from app import app
from flask_migrate import MigrateCommand
from flask_script import Manager, Server

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host="0.0.0.0", port="8000", use_debugger=True))

if __name__ == "__main__":
    manager.run()

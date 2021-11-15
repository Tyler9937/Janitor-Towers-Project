from .app import create_app

APP = create_app()

#gunicorn twitoff:APP -t 1200
#set FLASK_APP=Janitor_Towers:APP flask run
#pipenv shell
from .app import create_app

APP = create_app()

if __name__ == "__main__":
    APP.run(debug=True)

#gunicorn twitoff:APP -t 1200
#pipenv shell
#set FLASK_APP=Janitor_Towers:APP flask run
#pipenv shell
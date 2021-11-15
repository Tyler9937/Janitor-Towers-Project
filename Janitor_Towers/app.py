from flask import Flask, request, render_template



moves = 0
# title, paragrame, player input, space
game_history = [{"type": "space", "text": " "},
                {"type": "space", "text": " "},
                {"type": "paragraph", "text": "Welcome to Janitor Towers's"},
                {"type": "title", "text": "Janitor's Room"},
                {"type": "space", "text": " "}]

# Initializing the Flask App
def create_app():
    app = Flask(__name__)

    
    @app.route('/')
    def my_form():
        
        global game_history
        global moves
        moves = 0

        return render_template('base.html', room_location="Janitor's Room", moves=moves, game_history=game_history)

    @app.route('/', methods=['POST'])
    def my_form_post():

        global game_history
        global moves
        input_text = request.form['text']
        room_location = input_text
        moves = moves + 1

        game_history.append({"type": "input", "text": "> " + input_text})
        game_history.append({"type": "space", "text": " "})

        return render_template('base.html', room_location=room_location, moves=moves, game_history=game_history)







    # @app.route('/index')
    # def index():

       
    #     return render_template('base.html', name='test')



    return app
    
from flask import Flask, request, render_template
from main_game import build_game, Game


moves = 0
game_history = []


# # Initializing the Flask App
# def create_app(): (while in debug mode)
app = Flask(__name__)

game = build_game()

# Landing Page Initializing game
@app.route('/')
def my_form():
    
    global game_history
    global moves

    game_history = [{"type": "space", "text": " "},
                    {"type": "space", "text": " "},
                    {"type": "paragraph", "text": "Welcome to Janitor Towers's"},
                    {"type": "title", "text": "Janitor's Room"},
                    {"type": "space", "text": " "}] 
    moves = 0
    
    # game_reset()

    return render_template('base.html', room_location=game.current_loc, moves=moves, game_history=game_history)


# Player input post request (how player will be interacting with the game)
@app.route('/', methods=['POST'])
def my_form_post():

    global game_history
    global moves
    input_text = request.form['text']
    moves = moves + 1

    # Send input text to be proceced by game logic
    
    room_location = game.current_loc
    game.describe()
    output_text = game.output_text
    
    game_on = True

    if game_on:
        # System for storing and displaying game history
        game_history.append({"type": "input", "text": "> " + input_text})
        game_history.append({"type": "space", "text": " "})

        for p in output_text:
            game_history.append({'type': "paragraph", "text": p})
        
        game_history.append({"type": "space", "text": " "})

    else:
        moves = 0
        game_history = [{"type": "space", "text": " "},
                        {"type": "space", "text": " "},
                        {"type": "paragraph", "text": "Welcome to Janitor Towers's"},
                        {"type": "title", "text": "Janitor's Room"},
                        {"type": "space", "text": " "}]

    return render_template('base.html', room_location=room_location, moves=moves, game_history=game_history)

#return app (while in debug mode)
    
if __name__ == "__main__":
    app.run(debug=True)
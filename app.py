from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def boggle_start():
    """Renders the starting page with a blank board"""
    board = boggle_game.make_board()
    session['board'] = board
    return render_template("base.html")

@app.route('/check-word')
def check_word():
    """Checks to see if word is on the board"""
    word = request.args['word']
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'result': response})

@app.route('/post-score', methods=['POST'])
def post_score():
    """Receives end score from front-end. Updates session high score and game count"""
    score = request.json['score']
    high_score = session.get('high-score', 0)
    games_played = session.get('games-played', 0)
    games_played += 1
    session['games-played'] = games_played

    if score > high_score:
        session['high-score'] = score
    return jsonify(score > high_score)
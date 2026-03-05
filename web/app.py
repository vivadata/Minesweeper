# app.py
import os
import sys

from flask import Flask, redirect, render_template, request, url_for

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.minesweeper import Minesweeper

app = Flask(__name__)

# Create a new game
game = Minesweeper(5, 5, 3)


@app.route("/")
def index():
    board = game.get_board()
    if game.is_winner():
        return render_template("index.html", board=board, message="🔥 You Win! 🔥")
    return render_template("index.html", board=board)


@app.route("/reveal/<int:row>/<int:col>")
def reveal(row, col):
    result = game.reveal(row, col)
    if result == "Game Over":
        return render_template(
            "index.html", board=game.board, message="🥲 Game Over! 🥲"
        )
    return redirect(url_for("index"))


@app.route("/restart")
def restart():
    game.restart()
    return redirect(url_for("index"))


if __name__ == "__main__": # pragma: no cover
    app.run(debug=True, port=int(os.environ.get("PORT", 8080)))

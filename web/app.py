# app.py
import os
import sys

from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine, URL, sql
from sqlalchemy.orm import sessionmaker

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.minesweeper import Minesweeper

app = Flask(__name__)


url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT")
)

# Instantiate a sql alchemy engine 
engine = create_engine(url)

# Create a new game
game = Minesweeper(5, 5, 3)

Session = sessionmaker(bind=engine)
session = Session()

@app.get("/db_health")
def db_health():
    # Verify database connection
    try:
        with engine.connect() as connection:
            connection.execute(sql.text("SELECT 1"))
        return "OK", 200
    except Exception as e:
        return f"Database connection error: {e}", 500


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
    app.run(debug=True, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0")

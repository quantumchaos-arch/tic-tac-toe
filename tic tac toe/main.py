from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random

# FastAPI app instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the allowed origins here
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # This allows all headers
)

# Game state
xState = [0] * 9
oState = [0] * 9
turn = 1  # 1 = Player X, 0 = Computer O

# Winning combinations
wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

# Data model for move input
class Move(BaseModel):
    index: int

# Utility function to check for a win
def check_win(state):
    for win in wins:
        if state[win[0]] + state[win[1]] + state[win[2]] == 3:
            return True
    return False

# Utility function to check for a tie
def check_tie():
    return all(xState[i] == 1 or oState[i] == 1 for i in range(9))

# Computer's move
def computer_move():
    available_moves = [i for i in range(9) if xState[i] == 0 and oState[i] == 0]
    return random.choice(available_moves)

@app.get("/")
def read_root():
    return {"message": "Welcome to Tic Tac Toe API!"}

# Endpoint to handle a player's move
@app.post("/move/")
def player_move(move: Move):
    global turn
    index = move.index

    if xState[index] == 0 and oState[index] == 0:
        if turn == 1:
            xState[index] = 1
            if check_win(xState):
                return {"winner": "X", "message": "X won the game!"}
            if check_tie():
                return {"winner": "Tie", "message": "It's a tie!"}
            turn = 0  # Switch turn to the computer
        else:
            return {"message": "Not player's turn"}

    return {"message": "Move registered", "xState": xState, "oState": oState, "turn": turn}

# Endpoint for the computer's move
@app.get("/computer/")
def computer_move_endpoint():
    global turn
    if turn == 0:
        move = computer_move()
        oState[move] = 1
        if check_win(oState):
            return {"winner": "O", "message": "O won the game!"}
        if check_tie():
            return {"winner": "Tie", "message": "It's a tie!"}
        turn = 1  # Switch turn back to the player
        return {"message": "Computer moved", "move": move, "xState": xState, "oState": oState, "turn": turn}
    else:
        return {"message": "Not computer's turn"}

# Endpoint to reset the game
@app.post("/reset/")
def reset_game():
    global xState, oState, turn
    xState = [0] * 9
    oState = [0] * 9
    turn = 1  # Player X goes first
    return {"message": "Game reset", "xState": xState, "oState": oState, "turn": turn}

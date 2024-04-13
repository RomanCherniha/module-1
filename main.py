from fastapi import FastAPI, HTTPException
from models import Board, Rook, Knight, Bishop, Queen, King, Pawn
from database import Database

app = FastAPI()
db = Database('game_history.db')
board = Board()  

@app.on_event("startup")
async def startup_db_client():
    await db.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await db.close()

def reset_board():
    board.grid = [[None] * 8 for _ in range(8)]  
    board.setup_board() 

@app.post("/start_game")
async def start_game():
    reset_board()
    return {"message": "Game started."}

@app.post("/move")
async def move(player: str, position_from: list[int], position_to: list[int]):
    piece = board.grid[position_from[0]][position_from[1]]
    if piece is None:
        raise HTTPException(status_code=400, detail="No piece at the starting position.")
    if piece.color != player:
        raise HTTPException(status_code=400, detail="You can't move opponent's piece.")
    if not board.move_piece(position_from, position_to):
        raise HTTPException(status_code=400, detail="Invalid move.")
    await db.insert_move(player, position_from, position_to)
    return {"message": "Move successful."}

@app.post("/end_game")
async def end_game():
    await db.close()
    reset_board()
    return {"message": "Game ended."}

@app.get("/get_board")
async def get_board():
    board_state = board.get_board_state()
    return {"board": board_state}
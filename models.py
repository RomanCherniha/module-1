from abc import ABC, abstractmethod


class Board:
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        self.grid[0] = [
            Rook('black'), Knight('black'), Bishop('black'), Queen('black'),
            King('black'), Bishop('black'), Knight('black'), Rook('black')
        ]
        self.grid[1] = [Pawn('black') for _ in range(8)]


        self.grid[7] = [
            Rook('white'), Knight('white'), Bishop('white'), Queen('white'),
            King('white'), Bishop('white'), Knight('white'), Rook('white')
        ]
        self.grid[6] = [Pawn('white') for _ in range(8)]

    def place_piece(self, piece, position):
        row, col = position
        self.grid[row][col] = piece

    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.grid[start_row][start_col]

        if piece is None:
            return False

        if not piece.validate_move(start, end, self):
            return False

        self.grid[end_row][end_col] = piece
        self.grid[start_row][start_col] = None
        return True

    def get_board_state(self):
        board_state = []

        for row_idx, row in enumerate(self.grid):
            board_row = []
            for col_idx, piece in enumerate(row):
                if piece is not None:
                    board_row.append({
                        "type": type(piece).__name__,
                        "color": piece.color,
                        "coordinates": f"{chr(col_idx + 97)}{8 - row_idx}"  
                    })
                else:
                    
                    board_row.append(f"{chr(col_idx + 97)}{8 - row_idx}")  
            board_state.append(board_row)

        return board_state






class Piece(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def validate_move(self, start, end, board):
        pass


class King(Piece):
    def validate_move(self, start, end, board):
        x_distance = abs(start[0] - end[0])
        y_distance = abs(start[1] - end[1])
        return x_distance <= 1 and y_distance <= 1


class Rook(Piece):
    def validate_move(self, start, end, board):
        return start[0] == end[0] or start[1] == end[1]


class Knight(Piece):
    def validate_move(self, start, end, board):
        x_distance = abs(start[0] - end[0])
        y_distance = abs(start[1] - end[1])
        return (x_distance == 2 and y_distance == 1) or (x_distance == 1 and y_distance == 2)


class Bishop(Piece):
    def validate_move(self, start, end, board):
        
        x_distance = abs(start[0] - end[0])
        y_distance = abs(start[1] - end[1])
        return x_distance == y_distance


class Queen(Piece):
    def validate_move(self, start, end, board):
        return Rook().validate_move(start, end, board) or Bishop().validate_move(start, end, board)


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.initial_row = 1 if color == 'black' else 6

    def validate_move(self, start, end, board):
        # Pawn moves forward one square, but captures diagonally
        direction = 1 if self.color == 'black' else -1
        x_distance = end[0] - start[0]
        y_distance = abs(end[1] - start[1])

        if x_distance == direction and y_distance == 0 and board.grid[end[0]][end[1]] is None:
            return True
        elif x_distance == direction and y_distance == 1 and board.grid[end[0]][end[1]] is not None:
            return True
        elif (x_distance == 2 * direction and y_distance == 0 and
              start[0] == self.initial_row and board.grid[end[0]][end[1]] is None):
            return True
        return False
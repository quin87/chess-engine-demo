import chess
import chess.svg
import sys
from PyQt5.QtSvg import QSvgWidget
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QCheckBox, QWidget, QLabel
from PyQt5 import QtCore


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()

        self.RANK_NAMES = ['8', '7', '6', '5', '4', '3', '2', '1']
        self.current_player=False

        self.setGeometry(500, 200, 1050, 730)
        self.selected_piece = None

        self.BOARD_SIZE = 720
        self.CELL_SIZE = self.BOARD_SIZE // 8
 
        self.initialize_board()
        self.updateBoard()

    def initialize_board(self):
        #board
        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setFixedHeight(10)
        self.widgetSvg.setFixedWidth(10)
        self.widgetSvg.setFixedSize(self.BOARD_SIZE, self.BOARD_SIZE)
        self.chessboard = chess.Board()
        #buttons
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Undo")
        self.b1.clicked.connect(self.undo)
        self.b1.setGeometry(720,10,170,80)
        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("New Game")
        self.b2.clicked.connect(self.newgame)
        self.b2.setGeometry(890,10,170,80)
        #checkbox
        self.checkbox = QCheckBox('Queen', self)
        self.checkbox.setGeometry(740,100,150,30)
        self.checkbox = QCheckBox('Rook', self)
        self.checkbox.setGeometry(890,100,150,30)
        self.checkbox = QCheckBox('Knight', self)
        self.checkbox.setGeometry(740,130,150,30)
        self.checkbox = QCheckBox('Bishop', self)
        self.checkbox.setGeometry(890,130,150,30)    
        self.label = QLabel("Promotion")
        self.label.setGeometry(740,160,200,200)
    def undo(self):
        self.chessboard.pop()
        self.updateBoard()
    def newgame(self):
        self.chessboard.reset()
        self.updateBoard()
    
    def updateBoard(self):
        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg) 

    def move_piece(self, move):
        "moving piece #push(Ne4)"
        self.chessboard.push(move)
        "updating board"
        self.updateBoard()

    def mousePressEvent(self, event):
        cell_size = self.CELL_SIZE
        col = event.x() // cell_size
        row = event.y() // cell_size 
        
        piecetype = self.chessboard.piece_at((7-row)*8+col) 
        #fix
        if col*row<cell_size:
            clicked_piece = chess.FILE_NAMES[col]+self.RANK_NAMES[row] 
        clicked_piece_color = piecetype.color if piecetype != None else "Null"
        print(row,col,clicked_piece,piecetype,clicked_piece,self.selected_piece,clicked_piece_color)

        if self.selected_piece:
            if self.selected_piece == clicked_piece:
                self.selected_piece = None 
                print("reset1")
            else:
                # Try to move the selected piece
                ucimove = self.selected_piece+clicked_piece
                #print(ucimove)
                #if clicked_piece[1] == "8" and piecetype == 1:
                    
                move = chess.Move.from_uci(ucimove)
                if self.chessboard.is_legal(move):
                    print("valid")
                    self.move_piece(move)
                    #self.current_player = True if self.current_player == False else False
                self.selected_piece = None
                print("reset")
        elif clicked_piece :#and clicked_piece_color == self.current_player:
            self.selected_piece = clicked_piece

        self.updateBoard()
        #print(self.chessboard)

def main():
    app = QApplication(sys.argv)
    game = MainWindow()
    game.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()    

    
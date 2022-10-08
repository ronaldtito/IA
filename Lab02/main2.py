import tkinter as tk
from tkinter import messagebox
from matplotlib.widgets import Button
import numpy as np
from functools import partial


class Node(object):
    def __init__(self, n):
        self.n = n
        self.evaluation = 0
        self.nodeBoard = np.zeros((self.n,self.n),dtype = int)
        children = []


class TicTacToe():
    
    def __init__(self, n):
        self.n = n


        #self.botones = [[None for i in range(self.n)] for j in range(self.n) ]
        
        #-----------
        self.board = Node(self.n)
        #juego = [[0,1,0],
        #        [-1,0,-1],
        #        [0,1,0]]

        #self.board.nodeBoard = self.copyBoard(juego,self.board.nodeBoard)
        self.botones = [[None for i in range(self.n)] for j in range(self.n) ]

        #----------Crear una Funcion------------------------------
        self.Start()
    def setDepth(self,Depth):
        self.Depth = Depth
    def tablero(self,Board,LeftFrame, turn):
        for i in range(self.n):
            for j in range(self.n):
                current_button = tk.Button(LeftFrame,
                               text = ' ',
                               font=("tahoma", 25, "bold"),
                               height = 3,
                               width = 8,
                               bg="gainsboro",
                               command=lambda i=i,j=j:self.checker(i,j,turn)) 
        
                current_button.grid(row = i+1, column = j+1)
                self.botones[i][j] = current_button
        Board.mainloop()

    def updateBoard(self):
        for i in range(len(self.board.nodeBoard)):
            for j in range(len(self.board.nodeBoard)):
                current_button = self.botones[i][j] 
                if self.board.nodeBoard[i][j] == 1:
                    current_button.config(text='X')
                    current_button.config(state=tk.DISABLED)
                elif self.board.nodeBoard[i][j] == -1:
                    current_button.config(text='O')
                    current_button.config(state=tk.DISABLED)
                else:
                    current_button.config(text=' ')
        #----------------------------------------------------------
        

    def copyBoard(self, A, B):
        for i in range(len(self.board.nodeBoard)):
            for j in range(len(self.board.nodeBoard)):
                B[i][j] = A[i][j]
        return B


    def checker(self, i,j,turn):
        print(f"You pressed button {i},{j}")
        current_button = self.botones[i][j] 
        node = Node(self.n)
        self.updateBoard()
        if turn == 1:
            current_button.config(text='X')
            current_button.config(state=tk.DISABLED)
            self.board.nodeBoard[i][j] = 1
            node.nodeBoard = self.copyBoard(self.board.nodeBoard,node.nodeBoard)
            best = self.MinMax(1,node,self.Depth,1)
            


        else:
            current_button.config(text='O')
            current_button.config(state=tk.DISABLED)
            self.board.nodeBoard[i][j] = -1
            node.nodeBoard = self.copyBoard(self.board.nodeBoard,node.nodeBoard)
            best = self.MinMax(-1,node,self.Depth,1)
        

        self.board.nodeBoard = self.copyBoard(best.nodeBoard,self.board.nodeBoard)
        
        for m in range(self.n):
            for n in range(self.n):
                current_button = self.botones[m][n]
                if self.board.nodeBoard[m][n]==1:
                    current_button.config(text='X')
                    current_button.config(state=tk.DISABLED)
                elif self.board.nodeBoard[m][n]==-1:
                    current_button.config(text='O')
                    current_button.config(state=tk.DISABLED)
                else:
                    current_button.config(text=' ')


        if self.winCodition(1) or self.winCodition(-1):
            box = messagebox.showinfo('Finish')

    def checking(self, node, player):
        counter = 0
        for i in range(self.n):
            TTT = True
            for j in range(self.n):
                if node.nodeBoard[i][j] != 0 and node.nodeBoard[i][j] != player:
                    TTT = False
                    break
            if TTT:
                counter = counter + 1

        for i in range(self.n):
            TTT = True
            for j in range(self.n):
                if node.nodeBoard[j][i] != 0 and node.nodeBoard[j][i] != player:
                    TTT = False
                    break
            if TTT:
                counter = counter + 1

        TTT = True
        for i in range(self.n):
            if node.nodeBoard[i][i] != 0 and node.nodeBoard[i][i] != player:
                TTT = False
                break
        if TTT:
            counter = counter + 1

        TTT = True
        for i in range(self.n):
            if node.nodeBoard[i][self.n - 1 - i] != 0 and node.nodeBoard[i][self.n - 1 - i] != player:
                TTT = False
                break
        if TTT:
            counter = counter + 1

        return counter
    
    def winCodition(self, player):
        win = None 
        #check rows
        for i in range(self.n):
            win = True
            for j in range(self.n):
                if self.board.nodeBoard[i][j] != player:
                    win = False
                    break
            if win:
                return win
        
        #check columns
        for i in range(self.n):
            win = True
            for j in range(self.n):
                if self.board.nodeBoard[j][i] != player:
                    win = False
                    break
            if win:
                return win

        #check Diagonals
        win = True
        for i in range(self.n):
            if self.board.nodeBoard[i][i] != player:
                win = False
                break
        if win:
            return win

        win = True
        for i in range(self.n):
            if self.board.nodeBoard[i][self.n - 1 - i] != player:
                win = False
                break
        if win:
            return win

        for i in range(self.n):
            for j in range(self.n):
                if self.board.nodeBoard[i][j] == 0:
                    return False
        

    def Player2(self, player):
        if player == 1:
            return -1
        else:
            return 1

    def Evaluation(self, node,player):

        player2 = self.Player2(player)

        node.evaluation = self.checking(node,player) - self.checking(node,player2)
        return node

    def findall(self,matrix,element):
        result = []
        for i in range(len(matrix)):
            for j in range (len(matrix)):
                if matrix[i][j] == element:
                    result.append((i,j))
        return result


    def MinMax(self,player, node, depth, maximize):
        print('entra min max\n',node.nodeBoard)

        if depth == 0 :
            _node = Node(self.n)
            _node = self.Evaluation(node,player)
            print('Nodo Hoja')
            print(_node.nodeBoard)#print nodo final hijos
            return _node

        player2 = self.Player2(player)
        


        if maximize:
            _node = Node(self.n)
            _node.nodeBoard = self.copyBoard(node.nodeBoard, _node.nodeBoard)
            child = self.findall(_node.nodeBoard,0)
            maxi = []
            for i in child:
                _node.nodeBoard = self.copyBoard(node.nodeBoard, _node.nodeBoard)
                _node.nodeBoard[i[0]][i[1]] = player2
                temp = self.MinMax(player2,_node,depth - 1, 0)
                maxi.append((temp,temp.evaluation))

            pos = maxi.index(max(maxi,key=lambda tup:tup[1])) 
            position =child[pos]
            print('Nodo Padre')
            print(node.nodeBoard)
            node.nodeBoard[position[0]][position[1]]=player2
            node.evaluation = maxi[pos][1]
            print('Mejor Opcion Maxi')
            print(node.nodeBoard)
            return node

        else:
            _node1 = Node(self.n)
            _node1.nodeBoard = self.copyBoard(node.nodeBoard, _node1.nodeBoard)
            child = self.findall(_node1.nodeBoard,0)
            mini = []
            for i in child:
                _node1.nodeBoard = self.copyBoard(node.nodeBoard, _node1.nodeBoard)
                _node1.nodeBoard[i[0]][i[1]] = player2
                temp = self.MinMax(player2,_node1,depth - 1, 1)
                mini.append((temp,temp.evaluation))

            pos = mini.index(min(mini,key=lambda tup:tup[1])) 
            position =child[pos]
            print('Nodo Padre')
            print(node.nodeBoard)
            node.nodeBoard[position[0]][position[1]]=player2
            node.evaluation = mini[pos][1]
            print('Mejor Opcion Mini')
            print(node.nodeBoard)
            return node


    def optimalMovement(self, depth,turn):
        
        player = turn
        node = Node(self.n)
        node.nodeBoard = self.copyBoard(self.board.nodeBoard,node.nodeBoard)
        print('inicio\n',node.nodeBoard)
        bestOption = self.MinMax(player,node,depth,1)
        print('inicio\n',node.nodeBoard)
        self.board.nodeBoard = self.copyBoard(self.board.nodeBoard,bestOption.nodeBoard)
        print('bestie\n',bestOption.nodeBoard)
        print ('best\n',node.nodeBoard)

    def Game(self,board,depth,turn):
        board.destroy()
        board = tk.Tk()
        LeftFrame = tk.Frame(board)
        LeftFrame.grid()

        botones = [[None for i in range(self.n)] for j in range(self.n) ]

        if(turn == 1):# para O
            self.tablero(board,LeftFrame,turn)
        else:
            node = Node(self.n)
            best = self.MinMax(-1,node,self.Depth,1)
            self.board.nodeBoard = self.copyBoard(best.nodeBoard,self.board.nodeBoard)
            self.tablero(board,LeftFrame,-1)
        

    def Start(self):

        selectPlayer = tk.Tk()
        maxDepth = 3#int(input('Ingrese Profundidad de arbol: \n'))
        self.Depth = maxDepth
        selectPlayer.title('Inicio')
        title = tk.Button(selectPlayer,text='Select X - O')
        X = tk.Button(selectPlayer, text = 'X' ,command=lambda:self.Game(selectPlayer,maxDepth,1),bd = 5)
        O = tk.Button(selectPlayer, text = 'O' ,command=lambda:self.Game(selectPlayer,maxDepth,-1),bd = 5)
           

        title.pack()
        X.pack()
        O.pack()

        selectPlayer.mainloop()


Game = TicTacToe(3)
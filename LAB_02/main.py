import tkinter as tk
import numpy as np


class Node(object):
    def __init__(self, n):
        self.n = n
        self.evaluation = 0
        self.nodeBoard = np.zeros((self.n,self.n),dtype = int)
        children = []


class TicTacToe():
    
    def __init__(self, n):
        self.n = n

        self.root = tk.Tk()
        self.LeftFrame = tk.Frame(self.root)
        self.LeftFrame.grid()

        self.botones = [[None for i in range(self.n)] for j in range(self.n) ]
        self.board = Node(self.n)
        juego = [[0,1,0],
                [-1,0,-1],
                [0,1,0]]

        self.board.nodeBoard = self.copyBoard(juego,self.board.nodeBoard)

        #----------Crear una Funcion------------------------------
        turn = 1


        for i in range(self.n):
            for j in range(self.n):
                current_button = tk.Button(self.LeftFrame,
                               text = ' ',
                               font=("tahoma", 25, "bold"),
                               height = 3,
                               width = 8,
                               bg="gainsboro",
                               command=lambda i=i,j=j:self.checker(i,j,turn)) 
        
                current_button.grid(row = i+1, column = j+1)
                self.botones[i][j] = current_button
        #----------------------------------------------------------
        #self.Start()

    def copyBoard(self, A, B):
        for i in range(len(self.board.nodeBoard)):
            for j in range(len(self.board.nodeBoard)):
                B[i][j] = A[i][j]
        return B


    def checker(self, i,j,turn):
        print(f"You pressed button {i},{j}")
        current_button = self.botones[i][j] 
        if turn == 1:
            current_button.config(text='X')
        else:
            current_button.config(text='O')

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
        print(node.nodeBoard)
        if depth == 0 :
            _node = self.Evaluation(node,player)
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
            temp1 = maxi[0]
            for i in range(1,len(maxi)):
                if temp1[1] < maxi[i][1]:
                    temp1 = maxi[i]

            _node = temp1[0]
            print('the last',_node.nodeBoard)
            return _node

        else:
            _node1 = Node(self.n)
            _node1.nodeBoard = self.copyBoard(node.nodeBoard, _node1.nodeBoard)
            child = self.findall(_node1.nodeBoard,0)
            mini = []
            for i in child:
                temp1 =Node(self.n)
                _node1.nodeBoard = self.copyBoard(node.nodeBoard, _node1.nodeBoard)
                _node1.nodeBoard[i[0]][i[1]] = player2
                print (_node1.nodeBoard)
                temp = self.MinMax(player2,_node1,depth - 1, 1)
                mini.append((temp,temp.evaluation))
            temp1 = mini[0]
            for i in range(1,len(mini)):
                if temp1[1] > mini[i][1]:
                    temp1 = mini[i]

            _node = temp1[0]    
            return _node


    def optimalMovement(self, depth):
        
        player = 1
        node = Node(self.n)
        node.nodeBoard = self.copyBoard(self.board.nodeBoard,node.nodeBoard)
        print('inicio',node.nodeBoard)
        bestOption = self.MinMax(player,node,depth,1)
        
        node.nodeBoard = self.copyBoard(node.nodeBoard,bestOption.nodeBoard)
        print('bestie',bestOption.nodeBoard)
        print ('best',node.nodeBoard)

    def Move(self):
        print('hola',np.count_nonzero(self.board.nodeBoard == 0))

    def Start(self):
        Player = input('Select Player X - O \n')
        maxDepth = int(input('Ingrese Profundidad de arbol: \n'))
        if Player == 'X':
            self.Move()
        else:
            self.Move()

        self.Move()
        self.root.mainloop()


Game = TicTacToe(3)
Game.optimalMovement(3)
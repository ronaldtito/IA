
juego = [[0,0,0],
        [0,0,0],
        [0,0,0]]

human = "x"
computadora = "o"

def printMatriz(matriz):
  print("Tablero\n")
  print("\t1\t2\t3\n")
  x = 0
  while x < 3:
    y = 0
    print(str(x+1), end="\t")
    while y < 3:
      print(str(matriz[x][y]), end="\t")
      #print ("\t")
      y += 1
    print("\n")
    x += 1

def movimiento(matriz ,jugador):
  print("CAMBIO")

  if jugador == "humano":
    x = int(input("insert pos fila: "))
    y = int(input("insert pos columna: "))
    matriz[x-1][y-1] = "x"
  else:
    print("movimiento computadora")
    matriz[x-1][y-1] = "o"

def start():
  run = True
  printMatriz(juego)
  while (run):
    movimiento(juego,"humano")
    printMatriz(juego)
    state = str(input("Continua jugando S/N : "))
    if(state == "N"):
      run = False
    
###################################################################

start()

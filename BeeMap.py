import math
import itertools
from operator import itemgetter
from time import time

class Colisiones:
    #constructor
    def __init__(self, listaAbejitas, mapGrid, contador = 0):
        self.contador = 0
        self.listaAbejitas = listaAbejitas
        self.mapGrid = mapGrid
        self.mapa = None
        if (len(listaAbejitas) > 1):
            self.hacerMapa()
        else:
            self.comparacionSimple()
        print ("El total de abejas individuales en peligro es: "+str(self.contador))
        
    #Calcular distancia entre 2 abejas
    def calcularDistancia(self, abeja1, abeja2):
        d = math.sqrt(((((abeja1[1]-abeja2[1])*111111)**2)+(((abeja1[0]-abeja2[0])*111111)**2)+((abeja1[2]-abeja2[2])**2)))
        if d <= 100: #Si la diferencia de distancia es menor o igual a 100 metros, estan en peligro
            if abeja1[3] == False:
                self.contador += 1
            if abeja2[3] == False:
                self.contador +=1
            abeja1[3] = True
            abeja2[3] = True

    def hacerMapa(self):
        ini = time()
        Xsorted = sorted(listaAbejitas, key=itemgetter(1))
        Ysorted = sorted(listaAbejitas, key=itemgetter(0))
        Xmax = Xsorted[-1][1]
        Xmin = Xsorted[0][1]
        Ymax = Ysorted[-1][0]
        Ymin = Ysorted[0][0]

        ordenY = []
        ordenX = []
        deltaY = abs(Ymax-Ymin)/self.mapGrid
        deltaX = (abs(Xmax)-abs(Xmin))/self.mapGrid
        primerY = Ymax
        primerX = Xmin

        for i in range(0,self.mapGrid+1):
            ordenY.append(primerY)
            ordenX.append(primerX)
            primerY -= deltaY
            primerX -= deltaX
            
        relleno = time()
        print("||| Haciendo el mapa sin rellenar: ", relleno-ini)
        for i in range(len(listaAbejitas)):
            abeja = listaAbejitas[i]
            x = abeja[1]
            y = abeja[0]
            j = self.mapGrid-1
            k = 0
            indiceX = 0
            indiceY = 0
            while j >= 0:
                if y > ordenY[j]:
                    j -= 1
                else:
                    indiceY = j
                    break
            while k < self.mapGrid:
                if x > ordenX[k]:
                    k += 1
                else:
                    indiceX = k
                    break
            mapa[indiceX][indiceY].append(abeja)
        fin = time()
        """
        contador = 0
        for i in range(len(mapa)):
            for j in range(len(mapa[i])):
                print ("Sector ",i,j," tiene ", len(mapa[i][j]))
                contador += len(mapa[i][j])
        """
        self.mapa = mapa

        #print("el total de abejas es: "+str(contador))
        print("|| El mapa ha tardado: ", fin-ini)
        ini2 = time()
        self.comparacionEnMapa()
        fin2 = time()
        print("| Calculando me he tardado: ", fin2-ini2)

    def comparacionSimple(self):
        for i in range(len(listaAbejitas)):
            for j in range(i + 1, len(listaAbejitas)):
                self.calcularDistancia(listaAbejitas.get(i),listaAbejitas.get(j))

    def comparacionEnMapa(self):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[i])):
                for k in range(len(self.mapa[i][j])):
                    bee1 = self.mapa[i][j][k]
                    if bee1[3] == False:
                        for l in range(k+1, len(self.mapa[i][j])):
                            bee2 = self.mapa[i][j][l]
                            self.calcularDistancia(bee1, bee2)
                                                
    


abejasAux = open("./datasets/ConjuntoDeDatosCon1000000abejas.txt").readlines()
#creacion del diccionario
listaAbejitas = []
for indice,abeja in enumerate(abejasAux):
    if indice == 0:
        continue
    abeja = abeja.split(",")
    listaAbejitas.append([float(abeja[1]), float(abeja[0]), float(abeja[2]), False])
#creacion de la matriz
mapa = []
mapGrid = 16
if len(listaAbejitas) > 10000:
    mapGrid = 64
for i in range(0,mapGrid):
    mapa.append([])
    for j in range (0,mapGrid):
        mapa[i].append([])
abejasAux = None
analizador = Colisiones(listaAbejitas,mapGrid)
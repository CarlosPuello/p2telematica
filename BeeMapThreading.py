import math
import itertools
import numpy as np
from operator import itemgetter
from time import time
import threading

class Colisiones:
    #constructor
    def __init__(self, listaAbejitas, mapGrid, contador = 0):
        self.contador = 0
        self.listaAbejitas = listaAbejitas
        self.mapGrid = mapGrid
        self.mapa = None
        if (len(listaAbejitas) > 1):
            self.dividirDataset()
        else:
            self.comparacionSimple()
        
        
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
    
    def dividirDataset(self):
        inicio = time()
        X = sorted(listaAbejitas, key=itemgetter(1)) #Sortear abejas según X
        mx = int(len(listaAbejitas)/4) #Mitad del arreglo X

        x1 = X[:mx] #Primer mitad de abejas ordenadas por X
        x2 = X[mx:2*mx] #Segunda mitad de abejas ordenadas por X
        x3 = X[2*mx: 3*mx]
        x4 = X[3*mx:]

        y1 = sorted(x1, key=itemgetter(0)) #Primer mitad de abejas ordenadas por Y
        y2 = sorted(x2, key=itemgetter(0)) #Segunda mitad de abejas ordenadas por Y
        y3 = sorted(x3, key=itemgetter(0))
        y4 = sorted(x4, key=itemgetter(0))
        my = int(len(y1)/2) #Mitad del arreglo Y

        data1 = y1[:my] #Primer octavo del dataset ordenado por X,Y
        data2 = y1[my:] #Segundo octavo del dataset ordenado por X,Y
        data3 = y2[:my] #Tercer octavo del dataset ordenado por X,Y
        data4 = y2[my:] #Cuarto octavo del dataset ordenado por X,Y
        data5 = y3[:my] #Quinto octavo del dataset ordenado por X,Y
        data6 = y3[my:] #Sexto octavo del dataset ordenado por X,Y
        data7 = y4[:my] #Septimo octavo del dataset ordenado por X,Y
        data8 = y4[my:] #Octavo octavo del dataset ordenado por X,Y

        print("Creo que tengo como ",my, " datos") #PUTOS TODOS

        hilo1 = threading.Thread(target=self.hacerMapa, args=([data1]))
        hilo2 = threading.Thread(target=self.hacerMapa, args=([data2]))
        hilo3 = threading.Thread(target=self.hacerMapa, args=([data3]))
        hilo4 = threading.Thread(target=self.hacerMapa, args=([data4]))
        hilo5 = threading.Thread(target=self.hacerMapa, args=([data5]))
        hilo6 = threading.Thread(target=self.hacerMapa, args=([data6]))
        hilo7 = threading.Thread(target=self.hacerMapa, args=([data7]))
        hilo8 = threading.Thread(target=self.hacerMapa, args=([data8]))
        
        hilos = [hilo1,hilo2,hilo3,hilo4,hilo5,hilo6,hilo7,hilo8]

        final = time()
        print("Creando los 8 grupos me he tardado ",final-inicio)
        inicio = time()
        for h in hilos:
            h.start()

        for h in hilos:
            h.join()
        final = time()
        print("Todos los hilos se han tardado",final-inicio)
        #print(self.contador)
            

    def hacerMapa(self, grupoAbejas, idH = 0):
        tam = int(self.mapGrid/2)
        ini = time()
        mapaGroup = []
        
        for i in range(0,tam):
            mapaGroup.append([])
            for j in range (0,tam):
                mapaGroup[i].append([])

        Xsorted = sorted(grupoAbejas, key=itemgetter(1))
        Ysorted = sorted(grupoAbejas, key=itemgetter(0))
        Xmax = Xsorted[-1][1]
        Xmin = Xsorted[0][1]
        Ymax = Ysorted[-1][0]
        Ymin = Ysorted[0][0]

        ordenY = []
        ordenX = []
        deltaY = abs(Ymax-Ymin)/tam
        deltaX = (abs(Xmax)-abs(Xmin))/tam
        primerY = Ymax
        primerX = Xmin

        for i in range(0, tam+1):
            ordenY.append(primerY)
            ordenX.append(primerX)
            primerY -= deltaY
            primerX -= deltaX

        for i in range(len(grupoAbejas)):
            abeja = grupoAbejas[i]
            x = abeja[1]
            y = abeja[0]
            j = tam
            k = 0
            indiceX = 0
            indiceY = 0
            
            for j in reversed(range(tam)):
                if y <= ordenY[j]:
                    indiceY = j
                    break

            for k in range(tam):
                if x <= ordenX[k]:
                    indiceX = k
                    break

            mapaGroup[indiceX][indiceY].append(abeja)
        endi = time()
        print("El hilo ",idH," se ha tardado ", endi-ini)
        self.comparacionEnMapa(mapaGroup)

    def comparacionSimple(self):
        for i in range(len(listaAbejitas)):
            for j in range(i + 1, len(listaAbejitas)):
                self.calcularDistancia(listaAbejitas.get(i),listaAbejitas.get(j))

    def comparacionEnMapa(self, localMap):
        for i in range(len(localMap)):
            for j in range(len(localMap[i])):
                for k in range(len(localMap[i][j])):
                    bee1 = localMap[i][j][k]
                    if bee1[3] == False:
                        for l in range(k+1, len(localMap[i][j])):
                            bee2 = localMap[i][j][l]
                            self.calcularDistancia(bee1, bee2)

inicio = time()                                    
abejasAux = open("./datasets/ConjuntoDeDatosCon1000000abejas.txt").readlines()
#creacion del diccionario
listaAbejitas = []

for indice,abeja in enumerate(abejasAux):
    if indice == 0:
        continue
    abeja = abeja.split(",")
    listaAbejitas.append([float(abeja[1]), float(abeja[0]), float(abeja[2]), False])

final = time()
print("Leyendo el archivo me he tardado ", final-inicio)
mapGrid = 16

if len(listaAbejitas) > 10000:
    mapGrid = 64
    
abejasAux = None
analizador = Colisiones(listaAbejitas,mapGrid)
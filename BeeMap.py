import math
import itertools
from time import time

class Abeja:
    #Constructor
    def __init__(self, latitud, longitud, altura, llave, peligro = False):
        self.longitud = longitud
        self.latitud = latitud
        self.altura = altura
        self.llave = llave
        self.peligro = peligro

class Colisiones:
    #constructor
    def __init__(self, diccionarioAbejitas, mapGrid, contador = 0):
        self.contador = 0
        self.diccionarioAbejitas = diccionarioAbejitas
        self.mapGrid = mapGrid
        self.mapa = None
        if (len(diccionarioAbejitas) > 1):
            self.hacerMapa()
        else:
            self.comparacionSimple()
        print ("El total de abejas individuales en peligro es: "+str(self.contador))
        
    #Calcular distancia entre 2 abejas
    def calcularDistancia(self, abeja1, abeja2):
        d = math.sqrt(((((abeja1.longitud-abeja2.longitud)*111111)**2)+(((abeja1.latitud-abeja2.latitud)*111111)**2)+((abeja1.altura-abeja2.altura)**2)))
        if d <= 100: #Si la diferencia de distancia es menor o igual a 100 metros, estan en peligro
            if abeja1.peligro == False:
                self.contador += 1
            if abeja2.peligro == False:
                self.contador +=1
            abeja1.peligro = True
            abeja2.peligro = True

    def hacerMapa(self):
        ini = time()
        key_maxX = max(diccionarioAbejitas.keys(), key=(lambda k: diccionarioAbejitas[k].longitud))
        key_minX = min(diccionarioAbejitas.keys(), key=(lambda k: diccionarioAbejitas[k].longitud))
        key_maxY = max(diccionarioAbejitas.keys(), key=(lambda k: diccionarioAbejitas[k].latitud))
        key_minY = min(diccionarioAbejitas.keys(), key=(lambda k: diccionarioAbejitas[k].latitud))

        Xmax = diccionarioAbejitas[key_maxX].longitud
        Xmin = diccionarioAbejitas[key_minX].longitud
        Ymax = diccionarioAbejitas[key_maxY].latitud
        Ymin = diccionarioAbejitas[key_minY].latitud
        print('Valor maximo en y: ',Ymax)
        print('Valor minimo en y: ',Ymin)
        print('Valor maximo en x: ',Xmax)
        print('Valor minimo en x: ',Xmin)
        ordenY = []
        deltaY = abs(Ymax-Ymin)/self.mapGrid
        primerY = Ymax
        for i in range(0,self.mapGrid+1):
            ordenY.append(primerY)
            primerY -= deltaY

        ordenX = []
        deltaX = (abs(Xmax)-abs(Xmin))/self.mapGrid
        primerX = Xmin
        for i in range(0,self.mapGrid+1):
            ordenX.append(primerX)
            primerX -= deltaX
        print ("Orden en x= "+ str(ordenX))
        print ("Orden en y= "+ str(ordenY))

        for i in range(len(diccionarioAbejitas)):
            abeja = diccionarioAbejitas.get(i)
            x = abeja.longitud
            y = abeja.latitud
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
        print("Me he demorao ", fin-ini)

        self.comparacionEnMapa()

    def comparacionSimple(self):
        for i in range(len(diccionarioAbejitas)):
            for j in range(i + 1, len(diccionarioAbejitas)):
                self.calcularDistancia(diccionarioAbejitas.get(i),diccionarioAbejitas.get(j))

    def comparacionEnMapa(self):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[i])):
                for k in range(len(self.mapa[i][j])):
                    bee1 = self.mapa[i][j][k]
                    if bee1.peligro == False:
                        for l in range(k+1, len(self.mapa[i][j])):
                            bee2 = self.mapa[i][j][l]
                            self.calcularDistancia(bee1, bee2)
                                                
    


abejasAux = open("./datasets/ConjuntoDeDatosCon1000000abejas.txt").readlines()
#creacion del diccionario
diccionarioAbejitas = {}
for indice,abeja in enumerate(abejasAux):
    if indice == 0:
        continue
    abeja = abeja.split(",")
    abejita = Abeja(float(abeja[1]),float(abeja[0]),float(abeja[2]),indice-1)
    diccionarioAbejitas[indice-1] = abejita
#creacion de la matriz
mapa = []
mapGrid = 16
if len(diccionarioAbejitas) > 10000:
    mapGrid = 64
for i in range(0,mapGrid):
    mapa.append([])
    for j in range (0,mapGrid):
        mapa[i].append([])

abejasAux = None
analizador = Colisiones(diccionarioAbejitas,mapGrid)
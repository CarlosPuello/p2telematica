# Proyecto 2 Tópicos en telemática

## Miembros y aportes

- [Carlos Daniel Puello Peña](https://youtu.be/3dqSU0BcusY)
- [Julianny Restrepo López](https://youtu.be/)
- [Santiago Elias Rodríguez Hawasly](https://youtu.be/)

## Algoritmo a utilizar:
Creación de mapas para chequeo de colisiones de Drones en tiempo real
![](https://i.imgur.com/t8momE0.png)
Imagen por Alberto Restrepo, Mauricio Toro para Universidad EAFIT

### Implementación secuencial:

[Código](https://github.com/CarlosPuello/p2telematica/blob/master/BeeMap.py)


## Diseño PCAM

### Particionado

![](https://i.imgur.com/A1W0zr8.png)

**T0:** Carga de datos de abejas y rejillas del mapa (ordenes)

**T1:** Selección individual de abeja

**T2:** Busqueda de orden en Y para la abeja

**T3:** Busqueda de orden en X para la abeja

**TF:** Guardado del mapa poblado con abejas

### Comunicaciones

![](https://i.imgur.com/fL3mZg1.png)

Modelo de comunicaciones

![](https://i.imgur.com/5QAS972.png)

Modelo particionado

### Aglomeración

**Iniciación de datos:** T0

**Guardado de datos:** TF

**Procesamiento de datos:** T1, T2, T3

**Clústeres de tareas:** [T0 - T1] - [T2] - [T3] - [TF]

### Mapeo

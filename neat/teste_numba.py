#from mapa.mapa import calcula_distancia
import time
from numba import jit
tempo_antes:float = time.time()


#calcula_distancia((17,37),(1,45))

#@jit (nopython=True)
def printa():
    for i in range(1000000):
        print(" ")
#or i in range(100000):
   # calcula_distancia((17,37),(1,45))

#for i in range(100000):
  #  calcula_distancia((17,37),(1,45))
printa()
printa()
printa()



print(f"tempo total: {time.time() - tempo_antes}")
from matrix import matriz
from random import random_si64

struct mapa:
    "Mapa para os individuos percorerrem."
     var x: Int
     var y: Int
     var matriz_mapa: matriz 
     var posicoes_grama: matriz
     
     fn __init__(inout self, x:Int, y:Int , obstaculo_chance: Float16 , terra_chance: Float16, grama_chance: Float16)->NoneType:
        self.x = x
        self.y = y
        self.matriz_mapa = matriz(Int(0),x, y)
    
     """Hfn atualizar(inout self, proba_nova_grama: Float16):
        for i in range(self.x* self.y):
            var nova_grama: Int = random_si64(0,2).value

            if nova_grama:
                x =."""
    
     fn printar_mapa(borrowed self)->NoneType:
        self.matriz_mapa.imprime_matriz()
    
     fn surroundings(inout self, posicao: StaticIntTuple, alcance: Int)->matriz:
        """Dada uma posição do mapa (y, x)
        retornar uma matriz de todos os blocos do mapa a "alcance" de distancia
        tem que conter o ponto (y, x)."""
        var arredores: matriz = matriz(Int(0), alcance*2+1, alcance*2+1)
        var contadores: Int = -1

        #para todos os Y
        for i in range(posicao[1]-alcance, posicao[1]+alcance+1):
            contadores += 1
            #para todos os X
            for j in range(posicao[0]-alcance, posicao[0]+alcance+1):
                #se estiver dentro do mapa
                if (i < 0 or i >= self.x) or (j < 0 or j >= self.y):
                    surroundings[contador].append(1)
                else:
                    surroundings[contador].append(self.mapa[i][j])
        
        return arredores
    
        fn get_posicoes_grama(borrowed self)->matriz:
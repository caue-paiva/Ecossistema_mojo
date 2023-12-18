from ag.ag import AG
from individuos.individuo import CriarIndividuo, Individuo
from mapa.mapa import Mapa

import matplotlib.pyplot as plt
from copy import copy

import json
import os
import numpy as np

fitness_melhor_individuo = []
media_fitness_populacao = []
quantidade_de_grama = []

fintess_melhor_geracao = []

contador = 0
numero_do_grafico = 0

contador_quantidade = 500

melhor_de_todos: Individuo 

#mutacao_variavel = [0, 1, 1, 1, 0]
#index_mutacao = 0
#DELTA = 0.5
#delta_fitness = 0

contador_variavel = 0
contador_variavel_qtd = 500

ag = AG()

def Ordernar(individuos):
    def criterio_de_ordenacao(individuo):
        return individuo.quantidade

    return sorted(individuos, key=criterio_de_ordenacao, reverse=True)

def melhor_individuo(individuo1: Individuo, individuo2: Individuo):
    if individuo1.quantidade > individuo2.quantidade:
        return individuo1
    return individuo2

def cruzamento(individuo1: Individuo, individuo2: Individuo):
    gene_novo = individuo1.gene.copy()

    for i in range(len(gene_novo)): #para cada camada
        for neuronio in range(len(gene_novo[i]["weights"])):
            for weight in range(len(gene_novo[i]["weights"][neuronio])):
                gene_novo[i]["weights"][neuronio][weight] = (individuo1.gene[i]["weights"][neuronio][weight] + individuo2.gene[i]["weights"][neuronio][weight]) / 2

            for bias in range(len(gene_novo[i]["bias"][neuronio])):
                gene_novo[i]["bias"][neuronio][bias] = (individuo1.gene[i]["bias"][neuronio][bias] + individuo2.gene[i]["bias"][neuronio][bias]) / 2

    return gene_novo


class Simulacao():
    mudanca_num_pop: int #mudanca na qntd de individuos, ocorre quando individuos muito ruims são removidos da pop
    MUTACAO_VARIAVEL:list[int] = [0, 2, 0, 0 ,2,0]
    # [0, 1, 0 ,0 ,1] , relativamente estável e com certos picos
    #[0, 2, 0, 0 ,2,0] instavel e varios picos
    mutacao_variavel_index:int 
    DELTA:float = 0.5
    geracoes_fit_estag: int
    

    def __init__(self) -> None:
        self.mudanca_num_pop = 0 #inicializa essas variaveis para 0, para ela poder ser usada na primeira vez
        self.geracoes_fit_estag = 0
        self.mutacao_variavel_index = 0
        pass

    def __mutacao_atual__(self)->int: #retorna qual o nivel de mutacao é requerido 
        return self.MUTACAO_VARIAVEL[self.mutacao_variavel_index]

    def nova_populacao(self, populacao: list[Individuo], tipo: int)->list:
        global fintess_melhor_geracao
        global fitness_melhor_individuo
        global quantidade_de_grama

        global melhor_de_todos

        populacao = Ordernar(populacao) #ordernar a população (melhores no inicio)

        nova_populacao: list[Individuo] = []

        media_dos_fitness: int = 0 #media do fitness da população

        ##---------------------Passar melhores---------------------
        melhor_da_populacao = populacao[0]

        if melhor_da_populacao.quantidade > melhor_de_todos.quantidade:
           melhor_de_todos = copy(melhor_da_populacao)

        posicao = self.mapa.posicao_disponivel(3) #pegar uma nova posição
        nova_populacao.append(CriarIndividuo(gene=melhor_de_todos.gene, posicao=posicao, tipo=tipo, modelo=self.modelo)) #colocar o melhor de todos na proxima geração
 
        posicao = self.mapa.posicao_disponivel(3) #pegar uma nova posição
        nova_populacao.append(CriarIndividuo(gene=melhor_da_populacao.gene, posicao=posicao, tipo=tipo, modelo=self.modelo)) #colocar o melhor da geração na prróximo geração
        tam_pop_antiga: int = len(populacao)
        #print(f"tam da população antes: {tam_pop_antiga}")
        
        fit_melhor_pop: int = melhor_da_populacao.quantidade
        #---------------------Cruzar---------------------
        #a melhor metade da população cruza com o melhor da geração
        gene_cruzar:list
        if melhor_da_populacao == melhor_de_todos:
           gene_cruzar = None
        else:
            gene_cruzar = melhor_da_populacao
        for i in range(int(len(populacao)/2)):
            media_dos_fitness += populacao[i].quantidade #calcula a media

            gene = cruzamento(gene_cruzar, populacao[i])

            posicao = self.mapa.posicao_disponivel(tipo) #pegar uma nova posição
            nova_populacao.append(CriarIndividuo(gene=gene, posicao=posicao, tipo=tipo, modelo=self.modelo)) #passar o cara mutado
        

        #a pior metade da população cruza com o melhor de todos
        for i in range(int(len(populacao)/2), len(populacao) - 12):
            media_dos_fitness += populacao[i].quantidade #calcula a media 
            if (populacao[i].quantidade < fit_melhor_pop/4):
                continue
            gene = cruzamento(gene_cruzar, populacao[i]) #cruzar com o melhor de todos

            posicao = self.mapa.posicao_disponivel(tipo) #pegar uma nova posição
            nova_populacao.append(CriarIndividuo(gene=gene, posicao=posicao, tipo=tipo, modelo=self.modelo)) #adicionar o novo cara na população
       
        for i in range(self.mudanca_num_pop):  #coloca novos indv para entrar no lugar dos piores retirados da populacao
            print("novo cara para compensar")
            posicao = self.mapa.posicao_disponivel(tipo)
            nova_populacao.append(CriarIndividuo(gene=gene_cruzar.gene, posicao=posicao, modelo=self.modelo, tipo=tipo))
       
        for i in range(10): #adiciona 10 individous aleatorios
            posicao = self.mapa.posicao_disponivel(tipo)
            nova_populacao.append(CriarIndividuo(gene=None, posicao=posicao, modelo=self.modelo, tipo=tipo))


        #---------------------Grafico---------------------
        media_dos_fitness /= len(populacao) #calcula media
        media_fitness_populacao.append(media_dos_fitness) #adiciona media
        fitness_melhor_individuo.append(melhor_de_todos.quantidade)
        quantidade_de_grama.append(len(self.mapa.positions_withgrass))
        fintess_melhor_geracao.append(melhor_da_populacao.quantidade)
        self.mudanca_num_pop = abs(tam_pop_antiga - len(nova_populacao) )
        #print(f"mudanca na popula {self.mudanca_num_pop}")
        #print(f"tam da nova populacao {len(nova_populacao) }")
        return nova_populacao

    def Simulate(self):
        for acao in range(self.numero_de_acoes): #para cada ação
            for i in range(len(self.individuos)): #para cada indivíduo
                #---------------------Fazer uma ação---------------------
                inputs = self.mapa.inputs(self.individuos[i].posicao) #pegar os inputs para esse individuo

                predicao = self.individuos[i].network.predict(inputs) #fazer a predicao

                #ver qual ação deve ser feita
                acao = np.argmax(predicao)

                #fazer a ação
                nova_posicao, resultado = self.mapa.make_action(acao, self.individuos[i].posicao)

                #---------------------Resultado da ação---------------------
                self.individuos[i].posicao = nova_posicao #atualizar a posição

                if resultado == -1:
                    self.individuos[i].quantidade += 5 #ganhar 5 pontos se comeu
                else:
                    self.individuos[i].quantidade -= 1 #perder pontos se n comeu

    def StartPopulation(self, numero_de_individuos: int, modelo: list):
        individuos = []

        for _ in range(numero_de_individuos):
                posicao = self.mapa.posicao_disponivel(3)

                individuos.append(CriarIndividuo(gene=None, posicao=posicao, tipo=3, modelo=modelo))

        return individuos
            

    def StartSimulation(self, numero_de_geracoes: int, numero_de_individuos: int, numero_de_acoes: int, modelo: list):
        #---------------------Importações globais---------------------
        global melhor_de_todos

        global contador
        global contador_quantidade

        global contador_variavel
        global contador_variavel_qtd
        global index_mutacao
        global mutacao_variavel
        global delta_fitness

        #---------------------Informações---------------------
        self.numero_de_geracoes = numero_de_geracoes
        self.numero_de_indivudos = numero_de_individuos
        self.numero_de_acoes = numero_de_acoes
        self.modelo = modelo

        geracao = 0

        #---------------------Inicialização---------------------
        self.mapa = Mapa(50, 50, obstaculo_chance=0, terra_chance=0.2, grama_chance=0.8) #criar um mapa

        #criar os primeiros individuos
        self.individuos = self.StartPopulation(numero_de_individuos=numero_de_individuos, modelo=modelo)
        melhor_de_todos = self.individuos[0] #setar um individuo qualquer como o melhor de todos


        while(True):
            print("Na geração: ", geracao)

            geracao += 1
            #---------------------Grafico---------------------
            if contador == contador_quantidade:
                contador = 0

                self.Plotar_Grafico()

            contador += 1
            fit_melhor_antigo: int = melhor_de_todos.quantidade
            #---------------------Simular--------------------- 
            self.Simulate()
            
            #---------------------Nova Populacao---------------------
            self.mapa = Mapa(50, 50, obstaculo_chance=0, terra_chance=0.2, grama_chance=0.8) #criar um mapa novo (resetar as gramas)

            self.individuos = self.nova_populacao(self.individuos, self.individuos[0].tipo)    
            
            fit_novo_melhor: int = melhor_de_todos.quantidade 

            mudanca_fit = abs(fit_novo_melhor - fit_melhor_antigo)
            
            if mudanca_fit < self.DELTA:
                self.geracoes_fit_estag += 1

            tamanho_lista: int = len(self.MUTACAO_VARIAVEL)
            if  self.geracoes_fit_estag >= 10:
                self.mutacao_variavel_index  =  (self.mutacao_variavel_index + 1) %   tamanho_lista
                self.geracoes_fit_estag = 0
            
            
    def Plotar_Grafico(self):
        global melhor_de_todos
        global numero_do_grafico
        global fintess_melhor_geracao

        # Gerações (assumindo que cada elemento nas listas acima corresponde a uma geração)
        geracoes = list(range(1, len(fitness_melhor_individuo) + 1))

        # Criar o gráfico
        plt.plot(geracoes, fitness_melhor_individuo, label='Melhor Indivíduo')
        plt.plot(geracoes, media_fitness_populacao, label='Média da População')
        plt.plot(geracoes, fintess_melhor_geracao, label='Melhor da geracao')
        #plt.plot(geracoes, quantidade_de_grama, label='Grama')

        # Adicionar legendas e títulos
        plt.xlabel('Geração')
        plt.ylabel('Fitness')
        plt.title('Evolução do Fitness ao Longo das Gerações')
        plt.legend()

        diretorio = os.path.join("graficos", str(numero_do_grafico) + ".png")

        # Mostrar o gráfico
        plt.savefig(diretorio)
        plt.close()

        with open(os.path.join("genes", str(numero_do_grafico) + ".json"), "w") as f:
            json.dump(melhor_de_todos.gene, f)

        numero_do_grafico += 1 #atualizar o numero do grafico
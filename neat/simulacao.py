from ag.ag import AG
from individuos.individuo import CriarIndividuo, Individuo
from mapa.mapa import Mapa

import matplotlib.pyplot as plt

fitness_melhor_individuo = []
media_fitness_populacao = []
quantidade_de_grama = []

ag = AG()

def Ordenar(individuos: list[Individuo]):
    def criterio_de_ordenacao(individuo: Individuo):
        return individuo.vida

    return sorted(individuos, key=criterio_de_ordenacao)

def melhor_individuo(individuo1: Individuo, individuo2: Individuo):
    if individuo1.vida > individuo2.vida:
        return individuo1
    return individuo2

def cruzamento(individuo1: Individuo, individuo2: Individuo):
    gene_novo = individuo1.gene.copy()

    for i in range(len(individuo1.gene)):
        for j in range(len(individuo1.gene[i])):

            neuronio1_info: list = individuo1.gene[i][j]
            neuronio2_info: list = individuo2.gene[i][j]

            for k in range(0, len(neuronio1_info)):
                gene_novo[i][j][k][1] = (neuronio1_info[k][1] + neuronio2_info[k][1]) / 2

    return gene_novo




class Simulacao():
    def __init__(self) -> None:
        pass

    def torneio_de_dois(self, populacao: list[Individuo], tipo: int)->list:
        media_dos_fitness: int = 0
        for i in populacao:
            media_dos_fitness += i.vida
        
        media_dos_fitness /= len(populacao)
            
        media_fitness_populacao.append(media_dos_fitness)

        nova_populacao: list = []

        melhor: Individuo = populacao[0]

        #pegar o melhor indivíduo
        for i in range(0, len(populacao)): 
            if populacao[i].vida > melhor.vida:
                melhor = populacao[i]

        fitness_melhor_individuo.append(melhor.vida)

        melhor.vida = 1
        melhor.fome = 0
        
        nova_populacao.append(melhor) #colcoar o melhor de todos na proxima geração

        for i in range(len(populacao) - 1):
            #pai1 = melhor_individuo(populacao[random.randint(0, len(populacao) - 1)], populacao[random.randint(0, len(populacao) - 1)])
            #pai2 = melhor_individuo(populacao[random.randint(0, len(populacao) - 1)], populacao[random.randint(0, len(populacao) - 1)])

            pai1 = melhor
            pai2 = populacao[i]

            gene = cruzamento(pai1, pai2)

            gene = ag.mutate(gene) #mutar o gene

            posicao = self.mapa.posicao_disponivel(tipo)

            filho = CriarIndividuo(gene=gene, posicao=posicao, tipo=tipo)

            nova_populacao.append(filho)

        return nova_populacao
    
    def StartPopulation(self, numero_de_individuos: int, gene: list):
        individuos = []

        posicao = self.mapa.posicao_disponivel(3)

        for _ in range(numero_de_individuos):
                individuos.append(CriarIndividuo(gene=gene, posicao=posicao, tipo=3))

        return individuos

    def Simulate(self):
        for _ in range(self.numero_de_acoes):
            for i in range(len(self.individuos)):
                if (self.individuos[i].vida > 0):
                    self.individuos[i].fome += 0.1 #aumentar a fome

                    inputs = self.mapa.inputs(self.individuos[i].posicao) #pegar os inputs para esse individuo

                    predicao = self.individuos[i].network.predict(inputs) #fazer a predicao

                    #ver qual ação deve ser feita
                    acao = predicao.index(max(predicao))

                    #fazer a ação e pegar a nova posição do indivíduo após a ação
                    nova_posicao, resultado = self.mapa.make_action(acao, self.individuos[i].posicao)
                    self.individuos[i].posicao = nova_posicao 
                    
                    self.individuos[i].fome += resultado

                    if self.individuos[i].fome > 1: self.individuos[i].fome = 1
                    if self.individuos[i].fome < 0: self.individuos[i].fome = 0

                    #se o indivíduo está com fome
                    if self.individuos[i].fome == 1:
                        self.individuos[i].vida -= 0.1

                        if self.individuos[i].vida <= 0: #se o individuo morreu
                            self.mapa.mudar_valor(self.individuos[i].posicao, 0) #deixar aquela posicao como disponível

                            self.individuos[i].vida = 0
            

    def StartSimulation(self, numero_de_geracoes: int, numero_de_individuos: int, numero_de_acoes: int, gene_individuo: list):
        self.numero_de_geracoes = numero_de_geracoes
        self.numero_de_indivudos = numero_de_individuos
        self.numero_de_acoes = numero_de_acoes

        self.mapa = Mapa(20, 20, obstaculo_chance=0, terra_chance=0.80, grama_chance=0.20)

        self.individuos = self.StartPopulation(numero_de_individuos=numero_de_individuos, gene=gene_individuo)

        for geracao in range(self.numero_de_geracoes):
            quantidade_de_grama.append(len(self.mapa.positions_withgrass))
            print(f"Na geração {geracao}")

            self.Simulate()

            #self.mapa.atualizar(self.individuos) #atualizar o mapa

            self.mapa = Mapa(20, 20, obstaculo_chance=0, terra_chance=0.80, grama_chance=0.20)

            self.individuos = self.torneio_de_dois(self.individuos, self.individuos[0].tipo)
            
    def Results(self):
        # Gerações (assumindo que cada elemento nas listas acima corresponde a uma geração)
        geracoes = list(range(1, len(fitness_melhor_individuo) + 1))

        # Criar o gráfico
        plt.plot(geracoes, fitness_melhor_individuo, label='Melhor Indivíduo')
        plt.plot(geracoes, media_fitness_populacao, label='Média da População')

        # Adicionar legendas e títulos
        plt.xlabel('Geração')
        plt.ylabel('Fitness')
        plt.title('Evolução do Fitness ao Longo das Gerações')
        plt.legend()

        # Mostrar o gráfico
        plt.show()
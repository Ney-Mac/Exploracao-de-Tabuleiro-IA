import random
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

class Ambiente:
    def __init__(self, proporcao):
        self.tamanho = 10
        self.proporcao = proporcao
        self.matriz = self.inicializar()
        #self.estado_global

    def inicializar(self):
        linhaF = random.randint(0, 9)
        colunaF = random.randint(0, 9)
        matriz = [['L'] * self.tamanho for _ in range(self.tamanho)]

        for i in range(self.tamanho):
            for j in range(self.tamanho):
                r = random.random()
                if r < self.proporcao['B']:
                    matriz[i][j] = 'B'
                elif r < self.proporcao['B'] + self.proporcao['T']:
                    matriz[i][j] = 'T'
        matriz[linhaF][colunaF] = 'F'
        return matriz

    def imprimir(self, agentes):
        matriz_copia = self.matriz.copy()
        for agente in agentes:
            matriz_copia[agente.posicao[0]][agente.posicao[1]] = agente.nome

        for linha in matriz_copia:
            print(" ".join(linha))
        print()

class Agente:
    def __init__(self, nome, modelo):
        self.nome = nome
        self.modelo = modelo
        self.posicao = self.set_posicao()

    def set_posicao(self):
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)
        return (linha, coluna)

    def treinar(self, dados_treino, rotulos_treino):
        self.modelo.fit(dados_treino, rotulos_treino)

    def predizer(self, dados):
        return self.modelo.predict(dados)



def main():
    proporcao = {'B': 0.3, 'T': 0.2}

    ambiente = Ambiente(10, proporcao)
    #ambiente.imprimir([])

    # Carrega dados CSV
    data = pd.read_csv('../dataset/dataset.csv', delimiter=';')

    global_encoder = LabelEncoder()




main()
import random
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

class Ambiente:
    def __init__(self, proporcao):
        self.tamanho = 10
        self.proporcao = proporcao
        self.matriz_base = self.inicializar()
        self.matriz_compartilhada = self.inicializar_matriz_compartilhada()

    def inicializar_matriz_compartilhada(self):
        return [['N'] * self.tamanho for _ in range(self.tamanho)]

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
        matriz_copia = self.matriz_compartilhada.copy()
        for agente in agentes:
            matriz_copia[agente.posicao[0]][agente.posicao[1]] = agente.nome

        for linha in matriz_copia:
            print(" ".join(linha))
        print()

    def imprimir_matriz_base(self):
        for linha in self.matriz_base:
            print(" ".join(linha))
        print()

    def partilhar_informacao(self, linha, coluna, info):
        self.matriz_compartilhada[linha][coluna] = info

class Agente:
    def __init__(self, nome, modelo, dados_treino, rotulos_treino, encoder):
        self.nome = nome
        self.modelo = modelo
        self.encoder = encoder
        self.posicao = self.set_posicao()
        self.treinar(dados_treino, rotulos_treino)

    def set_posicao(self):
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)
        return (linha, coluna)

    def treinar(self, dados_treino, rotulos_treino):
        self.modelo.fit(dados_treino, rotulos_treino)
        print('Agente ', self.nome, ' Treinado')

    def testar(self, X_test):
        return self.modelo.predict(X_test)

    def predizer(self, dados):
        return self.modelo.predict(self.encoder.transform(dados))

    def get_celulas_vizinhas(self, ambiente):
        linha, coluna = self.posicao

        cima = ambiente.matriz_compartilhada[linha - 1][coluna] if (linha - 1 >= 0) else '-'
        baixo = ambiente.matriz_compartilhada[linha + 1][coluna] if (linha + 1 < ambiente.tamanho) else '-'
        esquerda = ambiente.matriz_compartilhada[linha][coluna - 1] if (coluna - 1 >= 0) else '-'
        direita = ambiente.matriz_compartilhada[linha][coluna + 1] if (coluna + 1 < ambiente.tamanho) else '-'

        return [esquerda, direita, cima, baixo]

    def mover(self, ambiente):
        linha, coluna = self.posicao
        celulas_vizinhas = self.get_celulas_vizinhas(ambiente)

        movimento = self.predizer(celulas_vizinhas)

        nova_posicao = (
            (linha + 1, coluna) if movimento == 'Baixo' else (
                (linha - 1, coluna) if movimento == 'Cima' else (
                    (linha, coluna + 1) if movimento == 'Direita' else
                    (linha, coluna - 1)
                )
            )
        )
        self.posicao = nova_posicao

        print(f'Agente {self.nome} moveu-se para {movimento}')
        self.interagir(ambiente)

    def enviar_informacao(self, ambiente):
        linha, coluna = self.posicao
        info = ambiente.matriz_base[linha][coluna]
        ambiente.partilhar_informacao(linha, coluna, info)

    def interagir(self, ambiente):
        linha, coluna = self.posicao
        celula_atual = ambiente.matriz_base[linha][coluna]

        print(f'Agente {self.nome} na posição {self.posicao}')
        print(f'Encontrou {celula_atual}')

        self.enviar_informacao(ambiente)

def main():
    proporcao = {'B': 0.3, 'T': 0.2}

    ambiente = Ambiente(proporcao)
    #ambiente.imprimir_matriz_base()
    #ambiente.imprimir([])

    # Carrega dados CSV
    data = pd.read_csv('../dados_treino/dataset.csv', delimiter=',')

    global_encoder = LabelEncoder()

    # Aplica o encoder para todas as colunas de entrada
    for column in data.columns:
        data[column] = global_encoder.fit_transform(data[column])

    # Separa os dados em treinamento e teste
    X = data[['Esquerda', 'Direita', 'Cima', 'Baixo']].values
    y = data['Acao'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=8)

    # Criar agentes
    num_agentes = 2
    agentes = []
    for i in range(num_agentes):
        modelo_agente = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=2000)
        agente = Agente(f'A{i + 1}', modelo_agente, X_test, y_test, global_encoder)
        agentes.append(agente)

    for agente in agentes:
        print(f'\nAgente {agente.nome}')
        print('Accuracy: ', accuracy_score(y_test, agente.testar(X_test)))

main()
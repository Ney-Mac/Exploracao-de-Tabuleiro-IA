import random
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pandas as pd

class Ambiente:
    def __init__(self, tamanho, proporcao_lbt):
        self.tamanho = tamanho
        self.proporcao_lbt = proporcao_lbt
        self.matriz = self.inicializar_ambiente()
        self.adicionar_elemento_aleatorio('F')

    def inicializar_ambiente(self):
        matriz = [['L'] * self.tamanho for _ in range(self.tamanho)]
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                r = random.random()
                if r < self.proporcao_lbt['B']:
                    matriz[i][j] = 'B'
                elif r < self.proporcao_lbt['B'] + self.proporcao_lbt['T']:
                    matriz[i][j] = 'T'
                elif r < self.proporcao_lbt['B'] + self.proporcao_lbt['T'] + self.proporcao_lbt['F']:
                    matriz[i][j] = 'F'
        return matriz

    def imprimir_ambiente(self, agentes):
        print("\n")
        for agente in agentes:
            valor_agente = self.matriz[agente.posicao[0]][agente.posicao[1]]
            self.matriz[agente.posicao[0]][agente.posicao[1]] = agente.nome

        for linha in self.matriz:
            print(" ".join(linha))

        for agente in agentes:
            self.matriz[agente.posicao[0]][agente.posicao[1]] = valor_agente

    def adicionar_elemento_aleatorio(self, elemento):
        i, j = random.randint(0, self.tamanho - 1), random.randint(0, self.tamanho - 1)
        self.matriz[i][j] = elemento

    def compartilhar_informacoes(self, agentes):
        informacoes_globais = {'bombas': [], 'tesouros': [], 'bandeiras': []}

        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.matriz[i][j] == 'B':
                    informacoes_globais['bombas'].append((i, j))
                elif self.matriz[i][j] == 'T':
                    informacoes_globais['tesouros'].append((i, j))
                elif self.matriz[i][j] == 'F':
                    informacoes_globais['bandeiras'].append((i, j))

        for agente in agentes:
            agente.compartilhar_info(informacoes_globais)

    def avaliar_resultados_abordagem_A(self, agentes):
        total_tesouros = sum([len(agente.informacoes_compartilhadas['tesouros']) for agente in agentes])
        tesouros_encontrados = sum([len(agente.informacoes_compartilhadas['tesouros_encontrados']) for agente in agentes])
        return tesouros_encontrados / total_tesouros if total_tesouros > 0 else 0

    def avaliar_resultados_abordagem_B(self, agentes):
        ambiente_total = self.tamanho * self.tamanho
        ambiente_explorado = sum([len(agente.informacoes_compartilhadas['celulas_exploradas']) for agente in agentes])
        return ambiente_explorado / ambiente_total

    def avaliar_resultados_abordagem_C(self, agentes):
        for agente in agentes:
            if agente.informacoes_compartilhadas['bandeira_encontrada']:
                return True
        return False

class Agente:
    def __init__(self, nome, modelo, encoder):
        self.nome = nome
        self.modelo = modelo
        self.posicao = (0, 0)
        self.informacoes_compartilhadas = {'bombas': [], 'tesouros': [], 'tesouros_encontrados': [],
                                           'celulas_exploradas': [], 'bandeira_encontrada': False}
        self.movimentos = []
        self.encoder = encoder

    def treinar_modelo(self, dados_treino, rotulos_treino):
        self.modelo.fit(dados_treino, rotulos_treino)

    def testar_modelo(self, dados_teste, rotulos_teste):
        resultado = self.modelo.predict(dados_teste)
        print('######## Resultado #######')
        print(resultado)

    def fazer_predicao(self, dados):
        rs = self.modelo.predict(dados.reshape(1, -1))
        return 'Cima' if 'A1' == rs else rs

    def mover(self, ambiente):
        linha, coluna = self.posicao

        cima = ambiente.matriz[linha - 1][coluna] if (linha - 1 >= 0) else '-'
        baixo = ambiente.matriz[linha + 1][coluna] if (linha + 1 < ambiente.tamanho) else '-'
        esquerda = ambiente.matriz[linha][coluna - 1] if (coluna - 1 >= 0) else '-'
        direita = ambiente.matriz[linha][coluna + 1] if (coluna + 1 < ambiente.tamanho) else '-'

        celulas_vizinhas = [esquerda, direita, baixo, cima]

        nova_posicao = self.posicao
        while nova_posicao == self.posicao or not (0 <= nova_posicao[0] < ambiente.tamanho and 0 <= nova_posicao[1] < ambiente.tamanho):
            predicao = self.fazer_predicao(self.encoder.transform(celulas_vizinhas))

            #print('Predicao ', self.nome, ' :', predicao)

            nova_posicao = (
                (linha + 1, coluna) if predicao == 'Baixo' else (
                    (linha - 1, coluna) if predicao == 'Cima' else (
                        (linha, coluna + 1) if predicao == 'Direita' else
                        (linha, coluna - 1)
                    )
                )
            )

        self.posicao = nova_posicao
        self.informacoes_compartilhadas['celulas_exploradas'].append(self.posicao)
        self.movimentos.append((self.nome, self.posicao))
        print(f"{self.nome} moveu-se para {self.posicao}")

    def interagir_ambiente(self, ambiente):
        linha, coluna = self.posicao
        celula_atual = ambiente.matriz[linha][coluna]

        if celula_atual == 'L':
            print(f"{self.nome} está em uma célula livre.")
        elif celula_atual == 'B':
            print(f"{self.nome} encontrou uma bomba e foi destruído!")
        elif celula_atual == 'T':
            print(f"{self.nome} encontrou um tesouro e ficou mais forte!")
            self.informacoes_compartilhadas['tesouros_encontrados'].append(self.posicao)

            if len(self.informacoes_compartilhadas['tesouros_encontrados']) >= 0.5 * int(
                    ambiente.proporcao_lbt['T'] * ambiente.tamanho ** 2):
                self.informacoes_compartilhadas['bandeira_encontrada'] = True
                print(f"{self.nome} encontrou a bandeira!")
        elif celula_atual == 'F':
            print(f"{self.nome} encontrou a bandeira!")

    def compartilhar_info(self, informacoes_compartilhadas):
        self.informacoes_compartilhadas['bombas'].extend(informacoes_compartilhadas['bombas'])
        self.informacoes_compartilhadas['tesouros'].extend(informacoes_compartilhadas['tesouros'])

    def tomar_acao(self, ambiente):
        self.mover(ambiente)
        self.interagir_ambiente(ambiente)

# Tamanho do ambiente e proporcoes
tamanho_ambiente = 10
proporcao_lbt = {'L': 0.5, 'B': 0.3, 'T': 0.2, 'F': 0.1}

# Inicializa o ambiente
ambiente = Ambiente(tamanho_ambiente, proporcao_lbt)
ambiente.imprimir_ambiente([])

# Carreg dados do CSV
data = pd.read_csv("../dataset/dataset.csv", delimiter=';')

# Inicializa o LabelEncoder
encoder = LabelEncoder()

# Aplica o encoder para todas as colunas de entrada
columns_to_encode = ['Esquerda', 'Direita', 'Baixo', 'Cima']
for column in columns_to_encode:
    data[column] = encoder.fit_transform(data[column])

# Separa os dados em treinamento e teste
X = data[['Esquerda', 'Direita', 'Baixo', 'Cima']].values
y = data['Acao'].values
X_train, X_test, y_train, y_test = train_test_split(X, y)

# Inicializa os agentes
agentes = []
num_agentes = 2
for i in range(num_agentes):
    modelo_agente = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=2000)
    agente = Agente(f'A{i + 1}', modelo_agente, encoder)
    agentes.append(agente)

# Treina os modelos dos agentes
for agente in agentes:
    agente.treinar_modelo(X_train, y_train)
    #agente.testar_modelo(X_test, y_test)

# Numero de passos na simulacao
num_passos_simulacao = 2
for passo in range(num_passos_simulacao):
    print(f"\nPasso {passo + 1}:\n")
    ambiente.compartilhar_informacoes(agentes)

    for agente in agentes:
        ambiente.imprimir_ambiente(agentes)
        agente.tomar_acao(ambiente)

# Avalia os resultados para cada abordagem
for abordagem in ['A', 'B', 'C']:
    resultado_abordagem = ambiente.avaliar_resultados_abordagem_A(agentes) if abordagem == 'A' else (
                          ambiente.avaliar_resultados_abordagem_B(agentes) if abordagem == 'B' else
                          ambiente.avaliar_resultados_abordagem_C(agentes))
    print(f"Resultados Abordagem {abordagem}: {resultado_abordagem}")
